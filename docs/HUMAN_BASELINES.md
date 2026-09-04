# Measured Human Baselines

AFB never fabricates human timing data. Author estimates are marked `source=estimated` and cannot activate official H50/H80 horizons.

## Collect an observed timing

Have a participant complete the public task under the same task instructions and record the observed elapsed time:

```bash
python -m afb.cli baseline-record \
  --samples human-timing-samples.json \
  --task-id A10-F-EXAMPLE \
  --seconds 1260 \
  --participant participant-01 \
  --population "professional operators"
```

Repeat for independent participants/completions. `baseline-record` stores only the values supplied to it; it does not generate or infer measurements.

## Compile measured baselines

```bash
python -m afb.cli baseline-compile \
  --samples human-timing-samples.json \
  --output human_baselines.json
```

The compiler calculates `n`, median completion time, and nearest-rank P80 for each task.

## Use them in an experiment

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --human-baselines human_baselines.json \
  ...
```

Only tasks with valid measured records are horizon-eligible. AFB reports H50/H80 as unavailable when the measured sample does not support a fit.

## Study requirements

For serious horizon claims, use the same task instructions and environment as the model evaluation, document the participant population and timing protocol, retain raw timing samples for auditability, and report the number of human observations. Public timing files may be contributed, but no baseline should be labeled `measured` without an actual observed completion.
