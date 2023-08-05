#!/usr/bin/env python3

import torch

EPS = 1e-8


class PrototypicalClassifier(torch.nn.Module):

    """
    Supports:
        * various number of shots per class.
        * euclidean, cosine, and custom distance metrics
        * embedding normalization
    """

    def __init__(
            self,
            support=None,
            labels=None,
            distance='euclidean',
            normalize=False,
            ):
        super(PrototypicalClassifier, self).__init__()
        self.distance = 'euclidean'
        self.normalize = normalize

        # Assign distance function
        if distance == 'euclidean':
            self.distance = PrototypicalClassifier.euclidean_distance
        elif distance == 'cosine':
            self.distance = PrototypicalClassifier.cosine_distance
            self.normalize = True
        else:
            self.distance = distance

        # Compute prototypes
        self.prototypes = None
        if support is not None and labels is not None:
            self.compute_prototypes_(support, labels)

    def compute_prototypes_(self, support, labels):
        """
        **Description**

        Computes and updates the prototypes given support embeddings and
        corresponding labels.

        * Might worth mvoing this to C++. (Unique + for loop + filter)
        * Make a differentiable version? (For Proto-MAML style algorithms)
        """
        classes = torch.unique(labels)
        prototypes = torch.zeros(classes.size(0), *support.shape[1:])
        for i, (cls, proto) in enumerate(zip(classes,
                                             prototypes.unbind(dim=0))):
            embeddings = support[labels == cls]
            proto[:] = embeddings.mean(dim=0)
        if self.normalize:
            prototypes = PrototypicalClassifier.normalize(prototypes)
        self.prototypes = prototypes
        return prototypes

    @staticmethod
    def cosine_distance(prototypes, queries):
        # Assumes both prototypes and queries are already normalized
        return - torch.mm(queries, prototypes.t())

    @staticmethod
    def euclidean_distance(prototypes, queries):
        n = prototypes.size(0)
        m = queries.size(0)
        prototypes = prototypes.unsqueeze(0).expand(m, n, -1)
        queries = queries.unsqueeze(1).expand(m, n, -1)
        distance = (prototypes - queries).pow(2).sum(dim=2)
        return distance

    @staticmethod
    def normalize(x, epsilon=EPS):
        x = x / (x.norm(p=2, dim=1, keepdim=True) + epsilon)
        return x

    def forward(self, x):
        assert self.prototypes is not None, \
            'Prototypes not computed, use compute_prototypes(support, labels)'
        if self.normalize:
            x = PrototypicalClassifier.normalize(x)
        return -self.distance(self.prototypes, x)
