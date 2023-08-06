# -*- coding: UTF-8 -*-
""""
Created on 08.04.20
Unit tests for samplers
:author:     Martin Dočekal
"""
import unittest
from torch.utils.data import Dataset
from windpytorchutils.samplers import IndicesSubsampler, SlidingBatchSampler
import torch

class MackUpDataset(Dataset):
    """
    Mock up dataset for testing.
    """

    def __init__(self, lenOfDataset):
        """
        Initialization of dataset.

        :param lenOfDataset: Number of samples.
        :type lenOfDataset: int
        """

        self.lDataset = lenOfDataset

    def __len__(self):
        return self.lDataset

    def __getitem__(self, item):
        return item


class TestIndicesSubsampler(unittest.TestCase):
    """
    Unit test of the IndicesSubsampler class.
    """

    def test_sampling(self):
        """
        Test the IndicesSubsampler.
        """
        lDataset = 1000
        sampler = IndicesSubsampler(source=MackUpDataset(lDataset), subsetLen=20)

        o = [x for x in sampler]
        self.assertLess(max(o), lDataset)
        self.assertEqual(len(o), 20)
        self.assertEqual(len(set(o)), 20)


class TestSlidingBatchSampler(unittest.TestCase):
    """
    Unit test of the SlidingBatchSampler class.
    """

    def test_init(self):

        with self.assertRaises(ValueError):
            SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(10)), 0, 3, False)

        with self.assertRaises(ValueError):
            SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(10)), 10, -3, False)

        with self.assertRaises(ValueError):
            SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(10)), 10, 2, "False")

    def test_len(self):
        """
        Test the length method.
        """

        lDataset = 100
        batchSize = 3
        stride = 2

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride, False)
        self.assertEqual(len(sampler), 50)

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride, True)
        self.assertEqual(len(sampler), 49)

        lDataset = 0
        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride, False)
        self.assertEqual(len(sampler), 0)

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride,
                                      True)
        self.assertEqual(len(sampler), 0)

        lDataset = 1
        batchSize = 3
        stride = 1
        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride,
                                      False)
        self.assertEqual(len(sampler), 1)

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), batchSize, stride,
                                      True)
        self.assertEqual(len(sampler), 0)

    def test_sampling(self):
        """
        Test the SlidingBatchSampler.
        """
        lDataset = 5

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 1, False)
        self.assertListEqual([x for x in sampler], [[0, 1], [1, 2], [2, 3], [3, 4]])

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 1, True)
        self.assertListEqual([x for x in sampler], [[0, 1], [1, 2], [2, 3], [3, 4]])

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 2, False)
        self.assertListEqual([x for x in sampler], [[0, 1], [2, 3], [4]])

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 2, True)
        self.assertListEqual([x for x in sampler], [[0, 1], [2, 3]])

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 3, 2, False)
        self.assertListEqual([x for x in sampler], [[0, 1, 2], [2, 3, 4]])

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 3, False)
        self.assertListEqual([x for x in sampler], [[0, 1], [3, 4]])

        lDataset = 0

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 3, False)
        self.assertListEqual([x for x in sampler], [])

        lDataset = 1

        sampler = SlidingBatchSampler(torch.utils.data.SequentialSampler(MackUpDataset(lDataset)), 2, 3, False)
        self.assertListEqual([x for x in sampler], [[0]])


if __name__ == '__main__':
    unittest.main()
