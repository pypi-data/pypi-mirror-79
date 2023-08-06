import torch
import torch.nn as nn


class Swapout(nn.Module):
    """
    The Swapout operator randomly swaps a pixel's features with the global average.

    Args:
        p: The probability of each pixel to be swapped.
    """

    def __init__(self, p=0.0):
        super(Swapout, self).__init__()

        if p < 0.0 or p > 1.0:
            raise ValueError('The probability of swapout must be within [0.0, 1.0]')

        self.p = p

    def forward(self, x):
        if self.training:
            # Modify the input at the training phase so that the expected outcome equals that at the testing phase
            g = torch.mean(x, dim=(2, 3), keepdim=True).expand_as(x)
            if self.p < 1.0:
                probs = torch.ones((x.size(0), 1, x.size(2), x.size(3)), dtype=x.dtype, device=x.device) * self.p
                mask = torch.bernoulli(probs).expand_as(x)
                x = mask * g + (1.0 - mask) * (x - g * self.p) / (1.0 - self.p)
            else:
                x = g
        else:
            # Keep the input as it is at the testing phase
            pass

        return x
