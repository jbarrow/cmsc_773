# CLPsych 2017 Challenge

To generate a sample of the data, run:

```
python -m scripts.sample -n 5000 -d "./**/**/TRAIN.txt"
```

Yes, the quotes are necessary. It has to be a mask that accesses both the
positive indices and the negative indices.
