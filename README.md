# TunixHack

The repo for the Google Tunix Hackathon

---

## Datasets

The existing datasets on HuggingFace is mostly sourced from DeepSeek R1.   
The issue with that is DeepSeek's reasoning traces are very long.

As this [paper](https://arxiv.org/abs/2502.12143v3), smaller models (<3B) sturggle to learn form strong reasoning traces (e.g. DS R1)

What's more, most reasoning datasets are focused on math and coding, with almost no dataset for creative writing, summary.etc.

#### data-bricks-thinking

We used Qwen3-14b to synthetically generate reasoning traces with question from the [databricks/databricks-dolly-15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k) dataset to create a high quality reasoning dataset called [data-bricks-thinking](https://huggingface.co/datasets/chimbiwide/databricks-thinking)

This process took 1 day 23 hours and 6 minutes on a 5070TI with a `Q4_K_M` quant of Qwen3-14b.
