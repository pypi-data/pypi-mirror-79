#!/usr/bin/env python3

"""
"""

import numpy as np
import torch
from torch import nn
import learn2learn as l2l
import pytorch_lightning as pl
from argparse import ArgumentParser


class LightningANIL(pl.LightningModule):

    adapt_steps = 5
    shots = 5
    ways = 5
    meta_lr = 0.001
    fast_lr = 0.1

    def __init__(
            self,
            features,
            classifier,
            **kwargs):
        super(LightningANIL, self).__init__()
        self.adapt_steps = kwargs.get("adapt_steps", LightningANIL.adapt_steps)
        self.shots = kwargs.get("shots", LightningANIL.shots)
        self.ways = kwargs.get("ways", LightningANIL.ways)
        self.meta_lr = kwargs.get("meta_lr", LightningANIL.meta_lr)
        self.fast_lr = kwargs.get("fast_lr", LightningANIL.fast_lr)
        self.features = features
        self.classifier = l2l.algorithms.MAML(classifier, lr=self.fast_lr)
        self.loss = nn.CrossEntropyLoss(reduction='mean')
        self.save_hyperparameters()

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--adapt_steps', type=int, default=LightningANIL.adapt_steps)
        parser.add_argument('--shots', type=int, default=LightningANIL.shots)
        parser.add_argument('--ways', type=int, default=LightningANIL.ways)
        parser.add_argument('--meta_lr', type=float, default=LightningANIL.meta_lr)
        parser.add_argument('--fast_lr', type=float, default=LightningANIL.fast_lr)
        return parser

    def training_step(self, batch, batch_idx):
        train_loss, train_accuracy = self.meta_learn(batch, batch_idx)
        result = pl.TrainResult(minimize=train_loss)
        result.log('train_loss', train_loss)
        result.log('train_accuracy', train_accuracy)
        return result

    def validation_step(self, batch, batch_idx):
        valid_loss, valid_accuracy = self.meta_learn(batch, batch_idx)
        result = pl.EvalResult()
        result.log('validation_loss', valid_loss)
        result.log('validation_accuracy', valid_accuracy)
        return result

    def testing_step(self, batch, batch_idx):
        test_loss, test_accuracy = self.meta_learn(batch, batch_idx)
        result = pl.EvalResult()
        result.log('test_loss', test_loss)
        result.log('test_accuracy', test_accuracy)
        return result

    def configure_optimizers(self):
        self.all_parameters = list(self.features.parameters()) + list(self.classifier.parameters())
        optimizer = torch.optim.Adam(self.all_parameters, lr=self.meta_lr)
        return optimizer

    @torch.enable_grad()
    def meta_learn(self, batch, batch_idx):
        learner = self.classifier.clone()
        data, labels = batch
        data = self.features(data)

        # Separate data into adaptation/evaluation sets
        adaptation_indices = np.zeros(data.size(0), dtype=bool)
        adaptation_indices[np.arange(self.shots * self.ways) * 2] = True
        evaluation_indices = torch.from_numpy(~adaptation_indices)
        adaptation_indices = torch.from_numpy(adaptation_indices)
        adaptation_data, adaptation_labels = data[adaptation_indices], labels[adaptation_indices]
        evaluation_data, evaluation_labels = data[evaluation_indices], labels[evaluation_indices]

        for step in range(self.adapt_steps):
            train_error = self.loss(learner(adaptation_data), adaptation_labels)
            learner.adapt(train_error)

        predictions = learner(evaluation_data)
        eval_loss = self.loss(predictions, evaluation_labels)
        eval_accuracy = accuracy(predictions, evaluation_labels)
        return eval_loss, eval_accuracy


def accuracy(predictions, targets):
    predictions = predictions.argmax(dim=1).view(targets.shape)
    return (predictions == targets).sum().float() / targets.size(0)

