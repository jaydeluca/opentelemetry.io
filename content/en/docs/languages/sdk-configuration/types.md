---
linkTitle: Types
weight: 10
aliases: [general-sdk-configuration]
---

<!-- BEGIN GENERATED: types SOURCE: opentelemetry-configuration -->

# Configuration Types

This page documents all configuration types for the OpenTelemetry SDK
declarative configuration.

## Stable Types

### Aggregation {#aggregation}

| Property                             | Type                                                                                        | Required? | Default Behavior    | Description                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------- | --------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `base2_exponential_bucket_histogram` | [`Base2ExponentialBucketHistogramAggregation`](#base2exponentialbuckethistogramaggregation) | `false`   | If omitted, ignore. | Configures the stream to collect data for the exponential histogram metric point, which uses a base-2 exponential formula to determine bucket boundaries and an integer scale parameter to control resolution. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#base2-exponential-bucket-histogram-aggregation> for details. |
| `default`                            | [`DefaultAggregation`](#defaultaggregation)                                                 | `false`   | If omitted, ignore. | Configures the stream to use the instrument kind to select an aggregation and advisory parameters to influence aggregation configuration parameters. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#default-aggregation> for details.                                                                                      |
| `drop`                               | [`DropAggregation`](#dropaggregation)                                                       | `false`   | If omitted, ignore. | Configures the stream to ignore/drop all instrument measurements. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#drop-aggregation> for details.                                                                                                                                                                            |
| `explicit_bucket_histogram`          | [`ExplicitBucketHistogramAggregation`](#explicitbuckethistogramaggregation)                 | `false`   | If omitted, ignore. | Configures the stream to collect data for the histogram metric point using a set of explicit boundary values for histogram bucketing. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#explicit-bucket-histogram-aggregation> for details                                                                                    |
| `last_value`                         | [`LastValueAggregation`](#lastvalueaggregation)                                             | `false`   | If omitted, ignore. | Configures the stream to collect data using the last measurement. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#last-value-aggregation> for details.                                                                                                                                                                      |
| `sum`                                | [`SumAggregation`](#sumaggregation)                                                         | `false`   | If omitted, ignore. | Configures the stream to collect the arithmetic sum of measurement values. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#sum-aggregation> for details.                                                                                                                                                                    |

**Constraints:**

• `additionalProperties`: `false`<br>• `minProperties`: `1`<br>•
`maxProperties`: `1`<br>

### AlwaysOffSampler {#alwaysoffsampler}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### AlwaysOnSampler {#alwaysonsampler}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### AttributeLimits {#attributelimits}

| Property                       | Type                                   | Required? | Default Behavior                       | Description                                                             |
| ------------------------------ | -------------------------------------- | --------- | -------------------------------------- | ----------------------------------------------------------------------- |
| `attribute_count_limit`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max attribute count. <br>Value must be non-negative.<br>      |
| `attribute_value_length_limit` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, there is no limit. | Configure max attribute value size. <br>Value must be non-negative.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### AttributeNameValue {#attributenamevalue}

| Property | Type                              | Required? | Default Behavior                           | Description                                                     |
| -------- | --------------------------------- | --------- | ------------------------------------------ | --------------------------------------------------------------- |
| `name`   | `string`                          | `true`    | Property is required and must be non-null. | The attribute name.<br>                                         |
| `type`   | [`AttributeType`](#attributetype) | `false`   | If omitted, string is used.                | The attribute type.<br>                                         |
| `value`  | `oneOf`                           | `true`    | Property is required and must be non-null. | The attribute value.<br>The type of value must match .type.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["name","value"]`<br>

### AttributeType {#attributetype}

**This is an enum type.**

| Value          | Description                    |
| -------------- | ------------------------------ |
| `bool`         | Boolean attribute value.       |
| `bool_array`   | Boolean array attribute value. |
| `double`       | Double attribute value.        |
| `double_array` | Double array attribute value.  |
| `int`          | Integer attribute value.       |
| `int_array`    | Integer array attribute value. |
| `string`       | String attribute value.        |
| `string_array` | String array attribute value.  |

### B3MultiPropagator {#b3multipropagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### B3Propagator {#b3propagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### BaggagePropagator {#baggagepropagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### Base2ExponentialBucketHistogramAggregation {#base2exponentialbuckethistogramaggregation}

| Property         | Type                                   | Required? | Default Behavior                  | Description                                                                                                                |
| ---------------- | -------------------------------------- | --------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `max_scale`      | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 20 is used.   | Configure the max scale factor.                                                                                            |
| `max_size`       | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 160 is used.  | Configure the maximum number of buckets in each of the positive and negative ranges, not counting the special zero bucket. |
| `record_min_max` | one of:<br>• `boolean`<br>• `null`<br> | `false`   | If omitted or null, true is used. | Configure whether or not to record min and max.                                                                            |

**Constraints:**

• `additionalProperties`: `false`<br>

### BatchLogRecordProcessor {#batchlogrecordprocessor}

| Property                | Type                                      | Required? | Default Behavior                           | Description                                                                                                                                      |
| ----------------------- | ----------------------------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `export_timeout`        | one of:<br>• `integer`<br>• `null`<br>    | `false`   | If omitted or null, 30000 is used.         | Configure maximum allowed time (in milliseconds) to export data. <br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br> |
| `exporter`              | [`LogRecordExporter`](#logrecordexporter) | `true`    | Property is required and must be non-null. | Configure exporter.                                                                                                                              |
| `max_export_batch_size` | one of:<br>• `integer`<br>• `null`<br>    | `false`   | If omitted or null, 512 is used.           | Configure maximum batch size. Value must be positive.<br>                                                                                        |
| `max_queue_size`        | one of:<br>• `integer`<br>• `null`<br>    | `false`   | If omitted or null, 2048 is used.          | Configure maximum queue size. Value must be positive.<br>                                                                                        |
| `schedule_delay`        | one of:<br>• `integer`<br>• `null`<br>    | `false`   | If omitted or null, 1000 is used.          | Configure delay interval (in milliseconds) between two consecutive exports. <br>Value must be non-negative.<br>                                  |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### BatchSpanProcessor {#batchspanprocessor}

| Property                | Type                                   | Required? | Default Behavior                           | Description                                                                                                                                      |
| ----------------------- | -------------------------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `export_timeout`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 30000 is used.         | Configure maximum allowed time (in milliseconds) to export data. <br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br> |
| `exporter`              | [`SpanExporter`](#spanexporter)        | `true`    | Property is required and must be non-null. | Configure exporter.                                                                                                                              |
| `max_export_batch_size` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 512 is used.           | Configure maximum batch size. Value must be positive.<br>                                                                                        |
| `max_queue_size`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 2048 is used.          | Configure maximum queue size. Value must be positive.<br>                                                                                        |
| `schedule_delay`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 5000 is used.          | Configure delay interval (in milliseconds) between two consecutive exports. <br>Value must be non-negative.<br>                                  |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### CardinalityLimits {#cardinalitylimits}

| Property                     | Type                                   | Required? | Default Behavior                                     | Description                                                                                                                 |
| ---------------------------- | -------------------------------------- | --------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `counter`                    | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for counter instruments.<br>                                                            |
| `default`                    | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 2000 is used.                    | Configure default cardinality limit for all instrument types.<br>Instrument-specific cardinality limits take priority. <br> |
| `gauge`                      | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for gauge instruments.<br>                                                              |
| `histogram`                  | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for histogram instruments.<br>                                                          |
| `observable_counter`         | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for observable_counter instruments.<br>                                                 |
| `observable_gauge`           | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for observable_gauge instruments.<br>                                                   |
| `observable_up_down_counter` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for observable_up_down_counter instruments.<br>                                         |
| `up_down_counter`            | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the value from .default is used. | Configure default cardinality limit for up_down_counter instruments.<br>                                                    |

**Constraints:**

• `additionalProperties`: `false`<br>

### ConsoleExporter {#consoleexporter}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ConsoleMetricExporter {#consolemetricexporter}

| Property                        | Type                                                                          | Required? | Default Behavior                               | Description                                  |
| ------------------------------- | ----------------------------------------------------------------------------- | --------- | ---------------------------------------------- | -------------------------------------------- |
| `default_histogram_aggregation` | [`ExporterDefaultHistogramAggregation`](#exporterdefaulthistogramaggregation) | `false`   | If omitted, explicit_bucket_histogram is used. | Configure default histogram aggregation.<br> |
| `temporality_preference`        | [`ExporterTemporalityPreference`](#exportertemporalitypreference)             | `false`   | If omitted, cumulative is used.                | Configure temporality preference.<br>        |

**Constraints:**

• `additionalProperties`: `false`<br>

### DefaultAggregation {#defaultaggregation}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### Distribution {#distribution}

**No properties.**

**Constraints:**

• `additionalProperties`: `{"type":"object"}`<br>• `minProperties`: `1`<br>

### DropAggregation {#dropaggregation}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExemplarFilter {#exemplarfilter}

**This is an enum type.**

| Value         | Description                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `always_off`  | ExemplarFilter which makes no measurements eligible for being an Exemplar.                                               |
| `always_on`   | ExemplarFilter which makes all measurements eligible for being an Exemplar.                                              |
| `trace_based` | ExemplarFilter which makes measurements recorded in the context of a sampled parent span eligible for being an Exemplar. |

### ExplicitBucketHistogramAggregation {#explicitbuckethistogramaggregation}

| Property         | Type                                   | Required? | Default Behavior                                                                               | Description                       |
| ---------------- | -------------------------------------- | --------- | ---------------------------------------------------------------------------------------------- | --------------------------------- |
| `boundaries`     | `array` of `number`                    | `false`   | If omitted, [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000] is used. | Configure bucket boundaries.<br>  |
| `record_min_max` | one of:<br>• `boolean`<br>• `null`<br> | `false`   | If omitted or null, true is used.                                                              | Configure record min and max.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExporterDefaultHistogramAggregation {#exporterdefaulthistogramaggregation}

**This is an enum type.**

| Value                                | Description                                                                           |
| ------------------------------------ | ------------------------------------------------------------------------------------- |
| `base2_exponential_bucket_histogram` | Use base2 exponential histogram as the default aggregation for histogram instruments. |
| `explicit_bucket_histogram`          | Use explicit bucket histogram as the default aggregation for histogram instruments.   |

### ExporterTemporalityPreference {#exportertemporalitypreference}

**This is an enum type.**

| Value        | Description                                                                                                                                          |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cumulative` | Use cumulative aggregation temporality for all instrument types.                                                                                     |
| `delta`      | Use delta aggregation for all instrument types except up down counter and asynchronous up down counter.                                              |
| `low_memory` | Use delta aggregation temporality for counter and histogram instrument types. Use cumulative aggregation temporality for all other instrument types. |

### GrpcTls {#grpctls}

| Property    | Type                                   | Required? | Default Behavior                                                                            | Description                                                                                                                                                                                         |
| ----------- | -------------------------------------- | --------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ca_file`   | one of:<br>• `string`<br>• `null`<br>  | `false`   | If omitted or null, system default certificate verification is used for secure connections. | Configure certificate used to verify a server's TLS credentials. <br>Absolute path to certificate file in PEM format.<br>                                                                           |
| `cert_file` | one of:<br>• `string`<br>• `null`<br>  | `false`   | If omitted or null, mTLS is not used.                                                       | Configure mTLS client certificate. <br>Absolute path to client certificate file in PEM format. If set, .client_key must also be set.<br>                                                            |
| `insecure`  | one of:<br>• `boolean`<br>• `null`<br> | `false`   | If omitted or null, false is used.                                                          | Configure client transport security for the exporter's connection. <br>Only applicable when .endpoint is provided without HTTP or HTTPS scheme. Implementations may choose to ignore .insecure.<br> |
| `key_file`  | one of:<br>• `string`<br>• `null`<br>  | `false`   | If omitted or null, mTLS is not used.                                                       | Configure mTLS private client key. <br>Absolute path to client key file in PEM format. If set, .client_certificate must also be set.<br>                                                            |

**Constraints:**

• `additionalProperties`: `false`<br>

### HttpTls {#httptls}

| Property    | Type                                  | Required? | Default Behavior                                                                            | Description                                                                                                                              |
| ----------- | ------------------------------------- | --------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `ca_file`   | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, system default certificate verification is used for secure connections. | Configure certificate used to verify a server's TLS credentials. <br>Absolute path to certificate file in PEM format.<br>                |
| `cert_file` | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, mTLS is not used.                                                       | Configure mTLS client certificate. <br>Absolute path to client certificate file in PEM format. If set, .client_key must also be set.<br> |
| `key_file`  | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, mTLS is not used.                                                       | Configure mTLS private client key. <br>Absolute path to client key file in PEM format. If set, .client_certificate must also be set.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### IncludeExclude {#includeexclude}

| Property   | Type                | Required? | Default Behavior                               | Description                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------------------- | --------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `excluded` | `array` of `string` | `false`   | If omitted, .included attributes are included. | Configure list of value patterns to exclude. Applies after .included (i.e. excluded has higher priority than included).<br>Values are evaluated to match as follows:<br> _If the value exactly matches.<br>_ If the value matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br> |
| `included` | `array` of `string` | `false`   | If omitted, all values are included.           | Configure list of value patterns to include.<br>Values are evaluated to match as follows:<br> _If the value exactly matches.<br>_ If the value matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br>                                                                            |

**Constraints:**

• `additionalProperties`: `false`<br>

### InstrumentType {#instrumenttype}

**This is an enum type.**

| Value                        | Description                               |
| ---------------------------- | ----------------------------------------- |
| `counter`                    | Synchronous counter instruments.          |
| `gauge`                      | Synchronous gauge instruments.            |
| `histogram`                  | Synchronous histogram instruments.        |
| `observable_counter`         | Asynchronous counter instruments.         |
| `observable_gauge`           | Asynchronous gauge instruments.           |
| `observable_up_down_counter` | Asynchronous up down counter instruments. |
| `up_down_counter`            | Synchronous up down counter instruments.  |

### JaegerPropagator {#jaegerpropagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### LastValueAggregation {#lastvalueaggregation}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### LoggerProvider {#loggerprovider}

| Property                                                | Type                                                                | Required? | Default Behavior                                                                     | Description                                             |
| ------------------------------------------------------- | ------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| `limits`                                                | [`LogRecordLimits`](#logrecordlimits)                               | `false`   | If omitted, default values as described in LogRecordLimits are used.                 | Configure log record limits. See also attribute_limits. |
| `processors`                                            | `array` of [`LogRecordProcessor`](#logrecordprocessor)              | `true`    | Property is required and must be non-null.                                           | Configure log record processors.                        |
| `logger_configurator/development`<br>**⚠ Experimental** | [`ExperimentalLoggerConfigurator`](#experimentalloggerconfigurator) | `false`   | If omitted, all loggers use default values as described in ExperimentalLoggerConfig. | Configure loggers.<br>                                  |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["processors"]`<br>

### LogRecordExporter {#logrecordexporter}

`LogRecordExporter` is an SDK extension plugin point.

| Property                                      | Type                                                            | Required? | Default Behavior    | Description                                            |
| --------------------------------------------- | --------------------------------------------------------------- | --------- | ------------------- | ------------------------------------------------------ |
| `console`                                     | [`ConsoleExporter`](#consoleexporter)                           | `false`   | If omitted, ignore. | Configure exporter to be console.                      |
| `otlp_grpc`                                   | [`OtlpGrpcExporter`](#otlpgrpcexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with gRPC transport.     |
| `otlp_http`                                   | [`OtlpHttpExporter`](#otlphttpexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with HTTP transport.     |
| `otlp_file/development`<br>**⚠ Experimental** | [`ExperimentalOtlpFileExporter`](#experimentalotlpfileexporter) | `false`   | If omitted, ignore. | Configure exporter to be OTLP with file transport.<br> |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### LogRecordLimits {#logrecordlimits}

| Property                       | Type                                   | Required? | Default Behavior                       | Description                                                                                                                       |
| ------------------------------ | -------------------------------------- | --------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `attribute_count_limit`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max attribute count. Overrides .attribute_limits.attribute_count_limit. <br>Value must be non-negative.<br>             |
| `attribute_value_length_limit` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, there is no limit. | Configure max attribute value size. Overrides .attribute_limits.attribute_value_length_limit. <br>Value must be non-negative.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### LogRecordProcessor {#logrecordprocessor}

`LogRecordProcessor` is an SDK extension plugin point.

| Property | Type                                                    | Required? | Default Behavior    | Description                              |
| -------- | ------------------------------------------------------- | --------- | ------------------- | ---------------------------------------- |
| `batch`  | [`BatchLogRecordProcessor`](#batchlogrecordprocessor)   | `false`   | If omitted, ignore. | Configure a batch log record processor.  |
| `simple` | [`SimpleLogRecordProcessor`](#simplelogrecordprocessor) | `false`   | If omitted, ignore. | Configure a simple log record processor. |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### MeterProvider {#meterprovider}

| Property                                               | Type                                                              | Required? | Default Behavior                                                                   | Description                                                                                                                                          |
| ------------------------------------------------------ | ----------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exemplar_filter`                                      | [`ExemplarFilter`](#exemplarfilter)                               | `false`   | If omitted, trace_based is used.                                                   | Configure the exemplar filter. <br>                                                                                                                  |
| `readers`                                              | `array` of [`MetricReader`](#metricreader)                        | `true`    | Property is required and must be non-null.                                         | Configure metric readers.                                                                                                                            |
| `views`                                                | `array` of [`View`](#view)                                        | `false`   | If omitted, no views are registered.                                               | Configure views. <br>Each view has a selector which determines the instrument(s) it applies to, and a configuration for the resulting stream(s).<br> |
| `meter_configurator/development`<br>**⚠ Experimental** | [`ExperimentalMeterConfigurator`](#experimentalmeterconfigurator) | `false`   | If omitted, all meters use default values as described in ExperimentalMeterConfig. | Configure meters.<br>                                                                                                                                |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["readers"]`<br>

### MetricProducer {#metricproducer}

`MetricProducer` is an SDK extension plugin point.

| Property     | Type                                                    | Required? | Default Behavior    | Description                                 |
| ------------ | ------------------------------------------------------- | --------- | ------------------- | ------------------------------------------- |
| `opencensus` | [`OpenCensusMetricProducer`](#opencensusmetricproducer) | `false`   | If omitted, ignore. | Configure metric producer to be opencensus. |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### MetricReader {#metricreader}

| Property   | Type                                            | Required? | Default Behavior    | Description                           |
| ---------- | ----------------------------------------------- | --------- | ------------------- | ------------------------------------- |
| `periodic` | [`PeriodicMetricReader`](#periodicmetricreader) | `false`   | If omitted, ignore. | Configure a periodic metric reader.   |
| `pull`     | [`PullMetricReader`](#pullmetricreader)         | `false`   | If omitted, ignore. | Configure a pull based metric reader. |

**Constraints:**

• `additionalProperties`: `false`<br>• `minProperties`: `1`<br>•
`maxProperties`: `1`<br>

### NameStringValuePair {#namestringvaluepair}

| Property | Type                                  | Required? | Default Behavior                                                                  | Description            |
| -------- | ------------------------------------- | --------- | --------------------------------------------------------------------------------- | ---------------------- |
| `name`   | `string`                              | `true`    | Property is required and must be non-null.                                        | The name of the pair.  |
| `value`  | one of:<br>• `string`<br>• `null`<br> | `true`    | Property must be present, but if null the behavior is dependent on usage context. | The value of the pair. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["name","value"]`<br>

### OpenCensusMetricProducer {#opencensusmetricproducer}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### OpenTelemetryConfiguration {#opentelemetryconfiguration}

| Property                                            | Type                                                          | Required? | Default Behavior                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------- | ------------------------------------------------------------- | --------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `attribute_limits`                                  | [`AttributeLimits`](#attributelimits)                         | `false`   | If omitted, default values as described in AttributeLimits are used. | Configure general attribute limits. See also tracer_provider.limits, logger_provider.limits.<br>                                                                                                                                                                                                                                                                                                                                         |
| `disabled`                                          | one of:<br>• `boolean`<br>• `null`<br>                        | `false`   | If omitted or null, false is used.                                   | Configure if the SDK is disabled or not.<br>                                                                                                                                                                                                                                                                                                                                                                                             |
| `distribution`                                      | [`Distribution`](#distribution)                               | `false`   | If omitted, distribution defaults are used.                          | Defines configuration parameters specific to a particular OpenTelemetry distribution or vendor.<br>This section provides a standardized location for distribution-specific settings<br>that are not part of the OpenTelemetry configuration model.<br>It allows vendors to expose their own extensions and general configuration options.<br>                                                                                            |
| `file_format`                                       | `string`                                                      | `true`    | Property is required and must be non-null.                           | The file format version.<br>Represented as a string including the SemVer major, minor version numbers (and optionally the meta tag). For example: "0.4", "1.0-rc.2", "1.0" (after stable release).<br>See <https://github.com/open-telemetry/opentelemetry-configuration/blob/main/VERSIONING.md> for more details.<br>The yaml format is documented at <https://github.com/open-telemetry/opentelemetry-configuration/tree/main/schema><br> |
| `log_level`                                         | [`SeverityNumber`](#severitynumber)                           | `false`   | If omitted, INFO is used.                                            | Configure the log level of the internal logger used by the SDK.<br>                                                                                                                                                                                                                                                                                                                                                                      |
| `logger_provider`                                   | [`LoggerProvider`](#loggerprovider)                           | `false`   | If omitted, a noop logger provider is used.                          | Configure logger provider.<br>                                                                                                                                                                                                                                                                                                                                                                                                           |
| `meter_provider`                                    | [`MeterProvider`](#meterprovider)                             | `false`   | If omitted, a noop meter provider is used.                           | Configure meter provider.<br>                                                                                                                                                                                                                                                                                                                                                                                                            |
| `propagator`                                        | [`Propagator`](#propagator)                                   | `false`   | If omitted, a noop propagator is used.                               | Configure text map context propagators.<br>                                                                                                                                                                                                                                                                                                                                                                                              |
| `resource`                                          | [`Resource`](#resource)                                       | `false`   | If omitted, the default resource is used.                            | Configure resource for all signals.<br>                                                                                                                                                                                                                                                                                                                                                                                                  |
| `tracer_provider`                                   | [`TracerProvider`](#tracerprovider)                           | `false`   | If omitted, a noop tracer provider is used.                          | Configure tracer provider.<br>                                                                                                                                                                                                                                                                                                                                                                                                           |
| `instrumentation/development`<br>**⚠ Experimental** | [`ExperimentalInstrumentation`](#experimentalinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                       | Configure instrumentation.<br>                                                                                                                                                                                                                                                                                                                                                                                                           |

**Constraints:**

• `additionalProperties`: `true`<br>• `required`: `["file_format"]`<br>

### OpenTracingPropagator {#opentracingpropagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### OtlpGrpcExporter {#otlpgrpcexporter}

| Property       | Type                                                     | Required? | Default Behavior                                   | Description                                                                                                                                                                                                                                                                                                                                   |
| -------------- | -------------------------------------------------------- | --------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `compression`  | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, none is used.                  | Configure compression.<br>Known values include: gzip, none. Implementations may support other compression algorithms.<br>                                                                                                                                                                                                                     |
| `endpoint`     | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, <http://localhost:4317> is used. | Configure endpoint.<br>                                                                                                                                                                                                                                                                                                                       |
| `headers`      | `array` of [`NameStringValuePair`](#namestringvaluepair) | `false`   | If omitted, no headers are added.                  | Configure headers. Entries have higher priority than entries from .headers_list.<br>If an entry's .value is null, the entry is ignored.<br>                                                                                                                                                                                                   |
| `headers_list` | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, no headers are added.          | Configure headers. Entries have lower priority than entries from .headers.<br>The value is a list of comma separated key-value pairs matching the format of OTEL_EXPORTER_OTLP_HEADERS. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options> for details.<br> |
| `timeout`      | one of:<br>• `integer`<br>• `null`<br>                   | `false`   | If omitted or null, 10000 is used.                 | Configure max time (in milliseconds) to wait for each export.<br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br>                                                                                                                                                                                                  |
| `tls`          | [`GrpcTls`](#grpctls)                                    | `false`   | If omitted, system default TLS settings are used.  | Configure TLS settings for the exporter.                                                                                                                                                                                                                                                                                                      |

**Constraints:**

• `additionalProperties`: `false`<br>

### OtlpGrpcMetricExporter {#otlpgrpcmetricexporter}

| Property                        | Type                                                                          | Required? | Default Behavior                                   | Description                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------- | --------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `compression`                   | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, none is used.                  | Configure compression.<br>Known values include: gzip, none. Implementations may support other compression algorithms.<br>                                                                                                                                                                                                                     |
| `default_histogram_aggregation` | [`ExporterDefaultHistogramAggregation`](#exporterdefaulthistogramaggregation) | `false`   | If omitted, explicit_bucket_histogram is used.     | Configure default histogram aggregation.<br>                                                                                                                                                                                                                                                                                                  |
| `endpoint`                      | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, <http://localhost:4317> is used. | Configure endpoint.<br>                                                                                                                                                                                                                                                                                                                       |
| `headers`                       | `array` of [`NameStringValuePair`](#namestringvaluepair)                      | `false`   | If omitted, no headers are added.                  | Configure headers. Entries have higher priority than entries from .headers_list.<br>If an entry's .value is null, the entry is ignored.<br>                                                                                                                                                                                                   |
| `headers_list`                  | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, no headers are added.          | Configure headers. Entries have lower priority than entries from .headers.<br>The value is a list of comma separated key-value pairs matching the format of OTEL_EXPORTER_OTLP_HEADERS. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options> for details.<br> |
| `temporality_preference`        | [`ExporterTemporalityPreference`](#exportertemporalitypreference)             | `false`   | If omitted, cumulative is used.                    | Configure temporality preference.<br>                                                                                                                                                                                                                                                                                                         |
| `timeout`                       | one of:<br>• `integer`<br>• `null`<br>                                        | `false`   | If omitted or null, 10000 is used.                 | Configure max time (in milliseconds) to wait for each export.<br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br>                                                                                                                                                                                                  |
| `tls`                           | [`GrpcTls`](#grpctls)                                                         | `false`   | If omitted, system default TLS settings are used.  | Configure TLS settings for the exporter.                                                                                                                                                                                                                                                                                                      |

**Constraints:**

• `additionalProperties`: `false`<br>

### OtlpHttpEncoding {#otlphttpencoding}

**This is an enum type.**

| Value      | Description               |
| ---------- | ------------------------- |
| `json`     | Protobuf JSON encoding.   |
| `protobuf` | Protobuf binary encoding. |

### OtlpHttpExporter {#otlphttpexporter}

| Property       | Type                                                     | Required? | Default Behavior                                                                                                    | Description                                                                                                                                                                                                                                                                                                                                   |
| -------------- | -------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `compression`  | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, none is used.                                                                                   | Configure compression.<br>Known values include: gzip, none. Implementations may support other compression algorithms.<br>                                                                                                                                                                                                                     |
| `encoding`     | [`OtlpHttpEncoding`](#otlphttpencoding)                  | `false`   | If omitted, protobuf is used.                                                                                       | Configure the encoding used for messages. <br>Implementations may not support JSON.<br>                                                                                                                                                                                                                                                       |
| `endpoint`     | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, the <http://localhost:4318/v1/{signal}> (where signal is 'traces', 'logs', or 'metrics') is used. | Configure endpoint, including the signal specific path.<br>                                                                                                                                                                                                                                                                                   |
| `headers`      | `array` of [`NameStringValuePair`](#namestringvaluepair) | `false`   | If omitted, no headers are added.                                                                                   | Configure headers. Entries have higher priority than entries from .headers_list.<br>If an entry's .value is null, the entry is ignored.<br>                                                                                                                                                                                                   |
| `headers_list` | one of:<br>• `string`<br>• `null`<br>                    | `false`   | If omitted or null, no headers are added.                                                                           | Configure headers. Entries have lower priority than entries from .headers.<br>The value is a list of comma separated key-value pairs matching the format of OTEL_EXPORTER_OTLP_HEADERS. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options> for details.<br> |
| `timeout`      | one of:<br>• `integer`<br>• `null`<br>                   | `false`   | If omitted or null, 10000 is used.                                                                                  | Configure max time (in milliseconds) to wait for each export.<br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br>                                                                                                                                                                                                  |
| `tls`          | [`HttpTls`](#httptls)                                    | `false`   | If omitted, system default TLS settings are used.                                                                   | Configure TLS settings for the exporter.                                                                                                                                                                                                                                                                                                      |

**Constraints:**

• `additionalProperties`: `false`<br>

### OtlpHttpMetricExporter {#otlphttpmetricexporter}

| Property                        | Type                                                                          | Required? | Default Behavior                                              | Description                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------- | --------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `compression`                   | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, none is used.                             | Configure compression.<br>Known values include: gzip, none. Implementations may support other compression algorithms.<br>                                                                                                                                                                                                                     |
| `default_histogram_aggregation` | [`ExporterDefaultHistogramAggregation`](#exporterdefaulthistogramaggregation) | `false`   | If omitted, explicit_bucket_histogram is used.                | Configure default histogram aggregation.<br>                                                                                                                                                                                                                                                                                                  |
| `encoding`                      | [`OtlpHttpEncoding`](#otlphttpencoding)                                       | `false`   | If omitted, protobuf is used.                                 | Configure the encoding used for messages. <br>Implementations may not support JSON.<br>                                                                                                                                                                                                                                                       |
| `endpoint`                      | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, <http://localhost:4318/v1/metrics> is used. | Configure endpoint.<br>                                                                                                                                                                                                                                                                                                                       |
| `headers`                       | `array` of [`NameStringValuePair`](#namestringvaluepair)                      | `false`   | If omitted, no headers are added.                             | Configure headers. Entries have higher priority than entries from .headers_list.<br>If an entry's .value is null, the entry is ignored.<br>                                                                                                                                                                                                   |
| `headers_list`                  | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, no headers are added.                     | Configure headers. Entries have lower priority than entries from .headers.<br>The value is a list of comma separated key-value pairs matching the format of OTEL_EXPORTER_OTLP_HEADERS. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options> for details.<br> |
| `temporality_preference`        | [`ExporterTemporalityPreference`](#exportertemporalitypreference)             | `false`   | If omitted, cumulative is used.                               | Configure temporality preference.<br>                                                                                                                                                                                                                                                                                                         |
| `timeout`                       | one of:<br>• `integer`<br>• `null`<br>                                        | `false`   | If omitted or null, 10000 is used.                            | Configure max time (in milliseconds) to wait for each export.<br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br>                                                                                                                                                                                                  |
| `tls`                           | [`HttpTls`](#httptls)                                                         | `false`   | If omitted, system default TLS settings are used.             | Configure TLS settings for the exporter.                                                                                                                                                                                                                                                                                                      |

**Constraints:**

• `additionalProperties`: `false`<br>

### ParentBasedSampler {#parentbasedsampler}

| Property                    | Type                  | Required? | Default Behavior                | Description                                      |
| --------------------------- | --------------------- | --------- | ------------------------------- | ------------------------------------------------ |
| `local_parent_not_sampled`  | [`Sampler`](#sampler) | `false`   | If omitted, always_off is used. | Configure local_parent_not_sampled sampler.<br>  |
| `local_parent_sampled`      | [`Sampler`](#sampler) | `false`   | If omitted, always_on is used.  | Configure local_parent_sampled sampler.<br>      |
| `remote_parent_not_sampled` | [`Sampler`](#sampler) | `false`   | If omitted, always_off is used. | Configure remote_parent_not_sampled sampler.<br> |
| `remote_parent_sampled`     | [`Sampler`](#sampler) | `false`   | If omitted, always_on is used.  | Configure remote_parent_sampled sampler.<br>     |
| `root`                      | [`Sampler`](#sampler) | `false`   | If omitted, always_on is used.  | Configure root sampler.<br>                      |

**Constraints:**

• `additionalProperties`: `false`<br>

### PeriodicMetricReader {#periodicmetricreader}

| Property             | Type                                           | Required? | Default Behavior                                                       | Description                                                                                                                                      |
| -------------------- | ---------------------------------------------- | --------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cardinality_limits` | [`CardinalityLimits`](#cardinalitylimits)      | `false`   | If omitted, default values as described in CardinalityLimits are used. | Configure cardinality limits.                                                                                                                    |
| `exporter`           | [`PushMetricExporter`](#pushmetricexporter)    | `true`    | Property is required and must be non-null.                             | Configure exporter.                                                                                                                              |
| `interval`           | one of:<br>• `integer`<br>• `null`<br>         | `false`   | If omitted or null, 60000 is used.                                     | Configure delay interval (in milliseconds) between start of two consecutive exports. <br>Value must be non-negative.<br>                         |
| `producers`          | `array` of [`MetricProducer`](#metricproducer) | `false`   | If omitted, no metric producers are added.                             | Configure metric producers.                                                                                                                      |
| `timeout`            | one of:<br>• `integer`<br>• `null`<br>         | `false`   | If omitted or null, 30000 is used.                                     | Configure maximum allowed time (in milliseconds) to export data. <br>Value must be non-negative. A value of 0 indicates no limit (infinity).<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### Propagator {#propagator}

| Property         | Type                                                 | Required? | Default Behavior                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | ---------------------------------------------------- | --------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `composite`      | `array` of [`TextMapPropagator`](#textmappropagator) | `false`   | If omitted, and .composite_list is omitted or null, a noop propagator is used.    | Configure the propagators in the composite text map propagator. Entries from .composite_list are appended to the list here with duplicates filtered out.<br>Built-in propagator keys include: tracecontext, baggage, b3, b3multi, Jaeger, ottrace. Known third party keys include: xray. <br>                                                                                                                                                                                                                                                                             |
| `composite_list` | one of:<br>• `string`<br>• `null`<br>                | `false`   | If omitted or null, and .composite is omitted or null, a noop propagator is used. | Configure the propagators in the composite text map propagator. Entries are appended to .composite with duplicates filtered out.<br>The value is a comma separated list of propagator identifiers matching the format of OTEL_PROPAGATORS. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/configuration/sdk-environment-variables.md#general-sdk-configuration> for details.<br>Built-in propagator identifiers include: tracecontext, baggage, b3, b3multi, Jaeger, ottrace. Known third party identifiers include: xray. <br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### PullMetricExporter {#pullmetricexporter}

`PullMetricExporter` is an SDK extension plugin point.

| Property                                       | Type                                                                            | Required? | Default Behavior    | Description                              |
| ---------------------------------------------- | ------------------------------------------------------------------------------- | --------- | ------------------- | ---------------------------------------- |
| `prometheus/development`<br>**⚠ Experimental** | [`ExperimentalPrometheusMetricExporter`](#experimentalprometheusmetricexporter) | `false`   | If omitted, ignore. | Configure exporter to be prometheus.<br> |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### PullMetricReader {#pullmetricreader}

| Property             | Type                                           | Required? | Default Behavior                                                       | Description                   |
| -------------------- | ---------------------------------------------- | --------- | ---------------------------------------------------------------------- | ----------------------------- |
| `cardinality_limits` | [`CardinalityLimits`](#cardinalitylimits)      | `false`   | If omitted, default values as described in CardinalityLimits are used. | Configure cardinality limits. |
| `exporter`           | [`PullMetricExporter`](#pullmetricexporter)    | `true`    | Property is required and must be non-null.                             | Configure exporter.           |
| `producers`          | `array` of [`MetricProducer`](#metricproducer) | `false`   | If omitted, no metric producers are added.                             | Configure metric producers.   |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### PushMetricExporter {#pushmetricexporter}

`PushMetricExporter` is an SDK extension plugin point.

| Property                                      | Type                                                                        | Required? | Default Behavior    | Description                                            |
| --------------------------------------------- | --------------------------------------------------------------------------- | --------- | ------------------- | ------------------------------------------------------ |
| `console`                                     | [`ConsoleMetricExporter`](#consolemetricexporter)                           | `false`   | If omitted, ignore. | Configure exporter to be console.<br>                  |
| `otlp_grpc`                                   | [`OtlpGrpcMetricExporter`](#otlpgrpcmetricexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with gRPC transport.<br> |
| `otlp_http`                                   | [`OtlpHttpMetricExporter`](#otlphttpmetricexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with HTTP transport.<br> |
| `otlp_file/development`<br>**⚠ Experimental** | [`ExperimentalOtlpFileMetricExporter`](#experimentalotlpfilemetricexporter) | `false`   | If omitted, ignore. | Configure exporter to be OTLP with file transport.<br> |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### Resource {#resource}

| Property                                      | Type                                                              | Required? | Default Behavior                                      | Description                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------- | ----------------------------------------------------------------- | --------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `attributes`                                  | `array` of [`AttributeNameValue`](#attributenamevalue)            | `false`   | If omitted, no resource attributes are added.         | Configure resource attributes. Entries have higher priority than entries from .resource.attributes_list.<br>                                                                                                                                                                                                                                                                                  |
| `attributes_list`                             | one of:<br>• `string`<br>• `null`<br>                             | `false`   | If omitted or null, no resource attributes are added. | Configure resource attributes. Entries have lower priority than entries from .resource.attributes.<br>The value is a list of comma separated key-value pairs matching the format of OTEL_RESOURCE_ATTRIBUTES. See <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/configuration/sdk-environment-variables.md#general-sdk-configuration> for details.<br> |
| `schema_url`                                  | one of:<br>• `string`<br>• `null`<br>                             | `false`   | If omitted or null, no schema URL is used.            | Configure resource schema URL.<br>                                                                                                                                                                                                                                                                                                                                                            |
| `detection/development`<br>**⚠ Experimental** | [`ExperimentalResourceDetection`](#experimentalresourcedetection) | `false`   | If omitted, resource detection is disabled.           | Configure resource detection.<br>                                                                                                                                                                                                                                                                                                                                                             |

**Constraints:**

• `additionalProperties`: `false`<br>

### Sampler {#sampler}

`Sampler` is an SDK extension plugin point.

| Property                                          | Type                                                                  | Required? | Default Behavior    | Description                                   |
| ------------------------------------------------- | --------------------------------------------------------------------- | --------- | ------------------- | --------------------------------------------- |
| `always_off`                                      | [`AlwaysOffSampler`](#alwaysoffsampler)                               | `false`   | If omitted, ignore. | Configure sampler to be always_off.           |
| `always_on`                                       | [`AlwaysOnSampler`](#alwaysonsampler)                                 | `false`   | If omitted, ignore. | Configure sampler to be always_on.            |
| `parent_based`                                    | [`ParentBasedSampler`](#parentbasedsampler)                           | `false`   | If omitted, ignore. | Configure sampler to be parent_based.         |
| `trace_id_ratio_based`                            | [`TraceIdRatioBasedSampler`](#traceidratiobasedsampler)               | `false`   | If omitted, ignore. | Configure sampler to be trace_id_ratio_based. |
| `composite/development`<br>**⚠ Experimental**     | [`ExperimentalComposableSampler`](#experimentalcomposablesampler)     | `false`   | If omitted, ignore. | Configure sampler to be composite.            |
| `jaeger_remote/development`<br>**⚠ Experimental** | [`ExperimentalJaegerRemoteSampler`](#experimentaljaegerremotesampler) | `false`   | If omitted, ignore. | Configure sampler to be jaeger_remote.        |
| `probability/development`<br>**⚠ Experimental**   | [`ExperimentalProbabilitySampler`](#experimentalprobabilitysampler)   | `false`   | If omitted, ignore. | Configure sampler to be probability.          |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### SeverityNumber {#severitynumber}

**This is an enum type.**

| Value    | Description                 |
| -------- | --------------------------- |
| `debug`  | debug, severity number 5.   |
| `debug2` | debug2, severity number 6.  |
| `debug3` | debug3, severity number 7.  |
| `debug4` | debug4, severity number 8.  |
| `error`  | error, severity number 17.  |
| `error2` | error2, severity number 18. |
| `error3` | error3, severity number 19. |
| `error4` | error4, severity number 20. |
| `fatal`  | fatal, severity number 21.  |
| `fatal2` | fatal2, severity number 22. |
| `fatal3` | fatal3, severity number 23. |
| `fatal4` | fatal4, severity number 24. |
| `info`   | info, severity number 9.    |
| `info2`  | info2, severity number 10.  |
| `info3`  | info3, severity number 11.  |
| `info4`  | info4, severity number 12.  |
| `trace`  | trace, severity number 1.   |
| `trace2` | trace2, severity number 2.  |
| `trace3` | trace3, severity number 3.  |
| `trace4` | trace4, severity number 4.  |
| `warn`   | warn, severity number 13.   |
| `warn2`  | warn2, severity number 14.  |
| `warn3`  | warn3, severity number 15.  |
| `warn4`  | warn4, severity number 16.  |

### SimpleLogRecordProcessor {#simplelogrecordprocessor}

| Property   | Type                                      | Required? | Default Behavior                           | Description         |
| ---------- | ----------------------------------------- | --------- | ------------------------------------------ | ------------------- |
| `exporter` | [`LogRecordExporter`](#logrecordexporter) | `true`    | Property is required and must be non-null. | Configure exporter. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### SimpleSpanProcessor {#simplespanprocessor}

| Property   | Type                            | Required? | Default Behavior                           | Description         |
| ---------- | ------------------------------- | --------- | ------------------------------------------ | ------------------- |
| `exporter` | [`SpanExporter`](#spanexporter) | `true`    | Property is required and must be non-null. | Configure exporter. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["exporter"]`<br>

### SpanExporter {#spanexporter}

`SpanExporter` is an SDK extension plugin point.

| Property                                      | Type                                                            | Required? | Default Behavior    | Description                                            |
| --------------------------------------------- | --------------------------------------------------------------- | --------- | ------------------- | ------------------------------------------------------ |
| `console`                                     | [`ConsoleExporter`](#consoleexporter)                           | `false`   | If omitted, ignore. | Configure exporter to be console.                      |
| `otlp_grpc`                                   | [`OtlpGrpcExporter`](#otlpgrpcexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with gRPC transport.     |
| `otlp_http`                                   | [`OtlpHttpExporter`](#otlphttpexporter)                         | `false`   | If omitted, ignore. | Configure exporter to be OTLP with HTTP transport.     |
| `otlp_file/development`<br>**⚠ Experimental** | [`ExperimentalOtlpFileExporter`](#experimentalotlpfileexporter) | `false`   | If omitted, ignore. | Configure exporter to be OTLP with file transport.<br> |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### SpanKind {#spankind}

**This is an enum type.**

| Value      | Description                 |
| ---------- | --------------------------- |
| `client`   | client, a client span.      |
| `consumer` | consumer, a consumer span.  |
| `internal` | internal, an internal span. |
| `producer` | producer, a producer span.  |
| `server`   | server, a server span.      |

### SpanLimits {#spanlimits}

| Property                       | Type                                   | Required? | Default Behavior                       | Description                                                                                                                       |
| ------------------------------ | -------------------------------------- | --------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `attribute_count_limit`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max attribute count. Overrides .attribute_limits.attribute_count_limit. <br>Value must be non-negative.<br>             |
| `attribute_value_length_limit` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, there is no limit. | Configure max attribute value size. Overrides .attribute_limits.attribute_value_length_limit. <br>Value must be non-negative.<br> |
| `event_attribute_count_limit`  | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max attributes per span event. <br>Value must be non-negative.<br>                                                      |
| `event_count_limit`            | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max span event count. <br>Value must be non-negative.<br>                                                               |
| `link_attribute_count_limit`   | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max attributes per span link. <br>Value must be non-negative.<br>                                                       |
| `link_count_limit`             | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 128 is used.       | Configure max span link count. <br>Value must be non-negative.<br>                                                                |

**Constraints:**

• `additionalProperties`: `false`<br>

### SpanProcessor {#spanprocessor}

`SpanProcessor` is an SDK extension plugin point.

| Property | Type                                          | Required? | Default Behavior    | Description                        |
| -------- | --------------------------------------------- | --------- | ------------------- | ---------------------------------- |
| `batch`  | [`BatchSpanProcessor`](#batchspanprocessor)   | `false`   | If omitted, ignore. | Configure a batch span processor.  |
| `simple` | [`SimpleSpanProcessor`](#simplespanprocessor) | `false`   | If omitted, ignore. | Configure a simple span processor. |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### SumAggregation {#sumaggregation}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### TextMapPropagator {#textmappropagator}

`TextMapPropagator` is an SDK extension plugin point.

| Property       | Type                                                | Required? | Default Behavior    | Description                               |
| -------------- | --------------------------------------------------- | --------- | ------------------- | ----------------------------------------- |
| `b3`           | [`B3Propagator`](#b3propagator)                     | `false`   | If omitted, ignore. | Include the Zipkin b3 propagator.         |
| `b3multi`      | [`B3MultiPropagator`](#b3multipropagator)           | `false`   | If omitted, ignore. | Include the Zipkin b3 multi propagator.   |
| `baggage`      | [`BaggagePropagator`](#baggagepropagator)           | `false`   | If omitted, ignore. | Include the w3c baggage propagator.       |
| `jaeger`       | [`JaegerPropagator`](#jaegerpropagator)             | `false`   | If omitted, ignore. | Include the Jaeger propagator.            |
| `ottrace`      | [`OpenTracingPropagator`](#opentracingpropagator)   | `false`   | If omitted, ignore. | Include the opentracing propagator.       |
| `tracecontext` | [`TraceContextPropagator`](#tracecontextpropagator) | `false`   | If omitted, ignore. | Include the w3c trace context propagator. |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### TraceContextPropagator {#tracecontextpropagator}

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### TraceIdRatioBasedSampler {#traceidratiobasedsampler}

| Property | Type                                  | Required? | Default Behavior                 | Description                   |
| -------- | ------------------------------------- | --------- | -------------------------------- | ----------------------------- |
| `ratio`  | one of:<br>• `number`<br>• `null`<br> | `false`   | If omitted or null, 1.0 is used. | Configure trace_id_ratio.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### TracerProvider {#tracerprovider}

| Property                                                | Type                                                                | Required? | Default Behavior                                                                     | Description                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `limits`                                                | [`SpanLimits`](#spanlimits)                                         | `false`   | If omitted, default values as described in SpanLimits are used.                      | Configure span limits. See also attribute_limits. |
| `processors`                                            | `array` of [`SpanProcessor`](#spanprocessor)                        | `true`    | Property is required and must be non-null.                                           | Configure span processors.                        |
| `sampler`                                               | [`Sampler`](#sampler)                                               | `false`   | If omitted, parent based sampler with a root of always_on is used.                   | Configure the sampler.<br>                        |
| `tracer_configurator/development`<br>**⚠ Experimental** | [`ExperimentalTracerConfigurator`](#experimentaltracerconfigurator) | `false`   | If omitted, all tracers use default values as described in ExperimentalTracerConfig. | Configure tracers.<br>                            |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["processors"]`<br>

### View {#view}

| Property   | Type                            | Required? | Default Behavior                           | Description                                                                                                                                                                                                         |
| ---------- | ------------------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `selector` | [`ViewSelector`](#viewselector) | `true`    | Property is required and must be non-null. | Configure view selector. <br>Selection criteria is additive as described in <https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/sdk.md#instrument-selection-criteria>.<br> |
| `stream`   | [`ViewStream`](#viewstream)     | `true`    | Property is required and must be non-null. | Configure view stream.                                                                                                                                                                                              |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["selector","stream"]`<br>

### ViewSelector {#viewselector}

| Property           | Type                                  | Required? | Default Behavior                                 | Description                                           |
| ------------------ | ------------------------------------- | --------- | ------------------------------------------------ | ----------------------------------------------------- |
| `instrument_name`  | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, all instrument names match.  | Configure instrument name selection criteria.<br>     |
| `instrument_type`  | [`InstrumentType`](#instrumenttype)   | `false`   | If omitted, all instrument types match.          | Configure instrument type selection criteria.<br>     |
| `meter_name`       | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, all meter names match.       | Configure meter name selection criteria.<br>          |
| `meter_schema_url` | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, all meter schema URLs match. | Configure meter schema URL selection criteria.<br>    |
| `meter_version`    | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, all meter versions match.    | Configure meter version selection criteria.<br>       |
| `unit`             | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, all instrument units match.  | Configure the instrument unit selection criteria.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ViewStream {#viewstream}

| Property                        | Type                                   | Required? | Default Behavior                                                           | Description                                                       |
| ------------------------------- | -------------------------------------- | --------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `aggregation`                   | [`Aggregation`](#aggregation)          | `false`   | If omitted, default is used.                                               | Configure aggregation of the resulting stream(s). <br>            |
| `aggregation_cardinality_limit` | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, the metric reader's default cardinality limit is used. | Configure the aggregation cardinality limit.<br>                  |
| `attribute_keys`                | [`IncludeExclude`](#includeexclude)    | `false`   | If omitted, all attribute keys are retained.                               | Configure attribute keys retained in the resulting stream(s).<br> |
| `description`                   | one of:<br>• `string`<br>• `null`<br>  | `false`   | If omitted or null, the instrument's origin description is used.           | Configure metric description of the resulting stream(s).<br>      |
| `name`                          | one of:<br>• `string`<br>• `null`<br>  | `false`   | If omitted or null, the instrument's original name is used.                | Configure metric name of the resulting stream(s).<br>             |

**Constraints:**

• `additionalProperties`: `false`<br>

## Experimental Types

> **Warning:** Experimental types are subject to breaking changes.

### ExperimentalComposableAlwaysOffSampler {#experimentalcomposablealwaysoffsampler}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalComposableAlwaysOnSampler {#experimentalcomposablealwaysonsampler}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalComposableParentThresholdSampler {#experimentalcomposableparentthresholdsampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                              | Required? | Default Behavior                           | Description                             |
| -------- | ----------------------------------------------------------------- | --------- | ------------------------------------------ | --------------------------------------- |
| `root`   | [`ExperimentalComposableSampler`](#experimentalcomposablesampler) | `true`    | Property is required and must be non-null. | Sampler to use when there is no parent. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["root"]`<br>

### ExperimentalComposableProbabilitySampler {#experimentalcomposableprobabilitysampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                  | Required? | Default Behavior                 | Description          |
| -------- | ------------------------------------- | --------- | -------------------------------- | -------------------- |
| `ratio`  | one of:<br>• `number`<br>• `null`<br> | `false`   | If omitted or null, 1.0 is used. | Configure ratio.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalComposableRuleBasedSampler {#experimentalcomposablerulebasedsampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                 | Required? | Default Behavior                        | Description                                                                                  |
| -------- | ------------------------------------ | --------- | --------------------------------------- | -------------------------------------------------------------------------------------------- |
| `rules`  | one of:<br>• `array`<br>• `null`<br> | `false`   | If omitted or null, no span is sampled. | The rules for the sampler, matched in order. If no rules match, the span is not sampled.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalComposableRuleBasedSamplerRule {#experimentalcomposablerulebasedsamplerrule}

> **Warning:** This type is experimental and subject to breaking changes.

A rule for ExperimentalComposableRuleBasedSampler. A rule can have multiple
match conditions - the sampler will be applied if all match. If no conditions
are specified, the rule matches all spans that reach it.

| Property             | Type                                                                                                                          | Required? | Default Behavior                           | Description                                                                                                                                                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `attribute_patterns` | [`ExperimentalComposableRuleBasedSamplerRuleAttributePatterns`](#experimentalcomposablerulebasedsamplerruleattributepatterns) | `false`   | If omitted, ignore.                        | Patterns to match against a single attribute. Non-string attributes are matched using their string representation:<br>for example, a pattern of "4\*" would match any http.response.status_code in 400-499. For array attributes, if any<br>item matches, it is considered a match.<br> |
| `attribute_values`   | [`ExperimentalComposableRuleBasedSamplerRuleAttributeValues`](#experimentalcomposablerulebasedsamplerruleattributevalues)     | `false`   | If omitted, ignore.                        | Values to match against a single attribute. Non-string attributes are matched using their string representation:<br>for example, a value of "404" would match the http.response.status_code 404. For array attributes, if any<br>item matches, it is considered a match.<br>            |
| `parent`             | `array` of [`ExperimentalSpanParent`](#experimentalspanparent)                                                                | `false`   | If omitted, ignore.                        | The parent span types to match.                                                                                                                                                                                                                                                         |
| `sampler`            | [`ExperimentalComposableSampler`](#experimentalcomposablesampler)                                                             | `true`    | Property is required and must be non-null. | The sampler to use for matching spans.                                                                                                                                                                                                                                                  |
| `span_kinds`         | `array` of [`SpanKind`](#spankind)                                                                                            | `false`   | If omitted, ignore.                        | The span kinds to match. If the span's kind matches any of these, it matches.                                                                                                                                                                                                           |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["sampler"]`<br>

### ExperimentalComposableRuleBasedSamplerRuleAttributePatterns {#experimentalcomposablerulebasedsamplerruleattributepatterns}

> **Warning:** This type is experimental and subject to breaking changes.

| Property   | Type                | Required? | Default Behavior                               | Description                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------------------- | --------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `excluded` | `array` of `string` | `false`   | If omitted, .included attributes are included. | Configure list of value patterns to exclude. Applies after .included (i.e. excluded has higher priority than included).<br>Values are evaluated to match as follows:<br> _If the value exactly matches.<br>_ If the value matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br> |
| `included` | `array` of `string` | `false`   | If omitted, all values are included.           | Configure list of value patterns to include.<br>Values are evaluated to match as follows:<br> _If the value exactly matches.<br>_ If the value matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br>                                                                            |
| `key`      | `string`            | `true`    | Property is required and must be non-null.     | The attribute key to match against.                                                                                                                                                                                                                                                                                                                            |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["key"]`<br>

### ExperimentalComposableRuleBasedSamplerRuleAttributeValues {#experimentalcomposablerulebasedsamplerruleattributevalues}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                | Required? | Default Behavior                           | Description                                                                                       |
| -------- | ------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `key`    | `string`            | `true`    | Property is required and must be non-null. | The attribute key to match against.                                                               |
| `values` | `array` of `string` | `true`    | Property is required and must be non-null. | The attribute values to match against. If the attribute's value matches any of these, it matches. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["key","values"]`<br>

### ExperimentalComposableSampler {#experimentalcomposablesampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property           | Type                                                                                            | Required? | Default Behavior    | Description                                   |
| ------------------ | ----------------------------------------------------------------------------------------------- | --------- | ------------------- | --------------------------------------------- |
| `always_off`       | [`ExperimentalComposableAlwaysOffSampler`](#experimentalcomposablealwaysoffsampler)             | `false`   | If omitted, ignore. | Configure sampler to be always_off.           |
| `always_on`        | [`ExperimentalComposableAlwaysOnSampler`](#experimentalcomposablealwaysonsampler)               | `false`   | If omitted, ignore. | Configure sampler to be always_on.            |
| `parent_threshold` | [`ExperimentalComposableParentThresholdSampler`](#experimentalcomposableparentthresholdsampler) | `false`   | If omitted, ignore. | Configure sampler to be parent_threshold.<br> |
| `probability`      | [`ExperimentalComposableProbabilitySampler`](#experimentalcomposableprobabilitysampler)         | `false`   | If omitted, ignore. | Configure sampler to be probability.          |
| `rule_based`       | [`ExperimentalComposableRuleBasedSampler`](#experimentalcomposablerulebasedsampler)             | `false`   | If omitted, ignore. | Configure sampler to be rule_based.           |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### ExperimentalContainerResourceDetector {#experimentalcontainerresourcedetector}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalGeneralInstrumentation {#experimentalgeneralinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                                  | Required? | Default Behavior                                                               | Description                                                                                                                                                                     |
| -------- | --------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `http`   | [`ExperimentalHttpInstrumentation`](#experimentalhttpinstrumentation) | `false`   | If omitted, defaults as described in ExperimentalHttpInstrumentation are used. | Configure instrumentations following the HTTP semantic conventions.<br>See HTTP semantic conventions: <https://opentelemetry.io/docs/specs/semconv/http/><br>                     |
| `peer`   | [`ExperimentalPeerInstrumentation`](#experimentalpeerinstrumentation) | `false`   | If omitted, defaults as described in ExperimentalPeerInstrumentation are used. | Configure instrumentations following the peer semantic conventions.<br>See peer semantic conventions: <https://opentelemetry.io/docs/specs/semconv/attributes-registry/peer/><br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalHostResourceDetector {#experimentalhostresourcedetector}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalHttpClientInstrumentation {#experimentalhttpclientinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property                    | Type                | Required? | Default Behavior                                      | Description                                                  |
| --------------------------- | ------------------- | --------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| `request_captured_headers`  | `array` of `string` | `false`   | If omitted, no outbound request headers are captured. | Configure headers to capture for outbound HTTP requests.<br> |
| `response_captured_headers` | `array` of `string` | `false`   | If omitted, no inbound response headers are captured. | Configure headers to capture for inbound HTTP responses.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalHttpInstrumentation {#experimentalhttpinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                                              | Required? | Default Behavior                                                                     | Description                                                                |
| -------- | --------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `client` | [`ExperimentalHttpClientInstrumentation`](#experimentalhttpclientinstrumentation) | `false`   | If omitted, defaults as described in ExperimentalHttpClientInstrumentation are used. | Configure instrumentations following the HTTP client semantic conventions. |
| `server` | [`ExperimentalHttpServerInstrumentation`](#experimentalhttpserverinstrumentation) | `false`   | If omitted, defaults as described in ExperimentalHttpServerInstrumentation are used. | Configure instrumentations following the HTTP server semantic conventions. |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalHttpServerInstrumentation {#experimentalhttpserverinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property                    | Type                | Required? | Default Behavior                              | Description                                                   |
| --------------------------- | ------------------- | --------- | --------------------------------------------- | ------------------------------------------------------------- |
| `request_captured_headers`  | `array` of `string` | `false`   | If omitted, no request headers are captured.  | Configure headers to capture for inbound HTTP requests.<br>   |
| `response_captured_headers` | `array` of `string` | `false`   | If omitted, no response headers are captures. | Configure headers to capture for outbound HTTP responses.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalInstrumentation {#experimentalinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property  | Type                                                                                          | Required? | Default Behavior                                                                        | Description                                                                                                                                                                                                                  |
| --------- | --------------------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cpp`     | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure C++ language-specific instrumentation libraries.                                                                                                                                                                   |
| `dotnet`  | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure .NET language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                  |
| `erlang`  | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Erlang language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                |
| `general` | [`ExperimentalGeneralInstrumentation`](#experimentalgeneralinstrumentation)                   | `false`   | If omitted, default values as described in ExperimentalGeneralInstrumentation are used. | Configure general SemConv options that may apply to multiple languages and instrumentations.<br>Instrumenation may merge general config options with the language specific configuration at .instrumentation.<language>.<br> |
| `go`      | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Go language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                    |
| `java`    | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Java language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                  |
| `js`      | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure JavaScript language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                            |
| `php`     | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure PHP language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                   |
| `python`  | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Python language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                |
| `ruby`    | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Ruby language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                  |
| `rust`    | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Rust language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                  |
| `swift`   | [`ExperimentalLanguageSpecificInstrumentation`](#experimentallanguagespecificinstrumentation) | `false`   | If omitted, instrumentation defaults are used.                                          | Configure Swift language-specific instrumentation libraries.<br>Each entry's key identifies a particular instrumentation library. The corresponding value configures it.<br>                                                 |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalJaegerRemoteSampler {#experimentaljaegerremotesampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property          | Type                                   | Required? | Default Behavior                           | Description                                                                                 |
| ----------------- | -------------------------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `endpoint`        | `string`                               | `true`    | Property is required and must be non-null. | Configure the endpoint of the Jaeger remote sampling service.                               |
| `initial_sampler` | [`Sampler`](#sampler)                  | `true`    | Property is required and must be non-null. | Configure the initial sampler used before first configuration is fetched.                   |
| `interval`        | one of:<br>• `integer`<br>• `null`<br> | `false`   | If omitted or null, 60000 is used.         | Configure the polling interval (in milliseconds) to fetch from the remote sampling service. |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`:
`["endpoint","initial_sampler"]`<br>

### ExperimentalLanguageSpecificInstrumentation {#experimentallanguagespecificinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `{"type":"object"}`<br>

### ExperimentalLoggerConfig {#experimentalloggerconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property           | Type                                   | Required? | Default Behavior                                          | Description                                                                                                                                                                                                                                |
| ------------------ | -------------------------------------- | --------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `disabled`         | one of:<br>• `boolean`<br>• `null`<br> | `false`   | If omitted or null, false is used.                        | Configure if the logger is enabled or not.<br>                                                                                                                                                                                             |
| `minimum_severity` | [`SeverityNumber`](#severitynumber)    | `false`   | If omitted, severity filtering is not applied.            | Configure severity filtering.<br>Log records with an non-zero (i.e. unspecified) severity number which is less than minimum_severity are not processed.<br>                                                                                |
| `trace_based`      | one of:<br>• `boolean`<br>• `null`<br> | `false`   | If omitted or null, trace based filtering is not applied. | Configure trace based filtering.<br>If true, log records associated with unsampled trace contexts traces are not processed. If false, or if a log record is not associated with a trace context, trace based filtering is not applied.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalLoggerConfigurator {#experimentalloggerconfigurator}

> **Warning:** This type is experimental and subject to breaking changes.

| Property         | Type                                                                                   | Required? | Default Behavior                                                                            | Description                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `default_config` | [`ExperimentalLoggerConfig`](#experimentalloggerconfig)                                | `false`   | If omitted, unmatched .loggers use default values as described in ExperimentalLoggerConfig. | Configure the default logger config used there is no matching entry in .logger_configurator/development.loggers. |
| `loggers`        | `array` of [`ExperimentalLoggerMatcherAndConfig`](#experimentalloggermatcherandconfig) | `false`   | If omitted, all loggers use .default_config.                                                | Configure loggers.                                                                                               |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalLoggerMatcherAndConfig {#experimentalloggermatcherandconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                    | Required? | Default Behavior                           | Description                                                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------- | --------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config` | [`ExperimentalLoggerConfig`](#experimentalloggerconfig) | `true`    | Property is required and must be non-null. | The logger config.                                                                                                                                                                                                                                               |
| `name`   | `string`                                                | `true`    | Property is required and must be non-null. | Configure logger names to match, evaluated as follows:<br><br> _If the logger name exactly matches.<br>_ If the logger name matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["name","config"]`<br>

### ExperimentalMeterConfig {#experimentalmeterconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property   | Type      | Required? | Default Behavior           | Description                               |
| ---------- | --------- | --------- | -------------------------- | ----------------------------------------- |
| `disabled` | `boolean` | `false`   | If omitted, false is used. | Configure if the meter is enabled or not. |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalMeterConfigurator {#experimentalmeterconfigurator}

> **Warning:** This type is experimental and subject to breaking changes.

| Property         | Type                                                                                 | Required? | Default Behavior                                                                          | Description                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------ | --------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `default_config` | [`ExperimentalMeterConfig`](#experimentalmeterconfig)                                | `false`   | If omitted, unmatched .meters use default values as described in ExperimentalMeterConfig. | Configure the default meter config used there is no matching entry in .meter_configurator/development.meters. |
| `meters`         | `array` of [`ExperimentalMeterMatcherAndConfig`](#experimentalmetermatcherandconfig) | `false`   | If omitted, all meters used .default_config.                                              | Configure meters.                                                                                             |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalMeterMatcherAndConfig {#experimentalmetermatcherandconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                  | Required? | Default Behavior                           | Description                                                                                                                                                                                                                                                   |
| -------- | ----------------------------------------------------- | --------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config` | [`ExperimentalMeterConfig`](#experimentalmeterconfig) | `true`    | Property is required and must be non-null. | The meter config.                                                                                                                                                                                                                                             |
| `name`   | `string`                                              | `true`    | Property is required and must be non-null. | Configure meter names to match, evaluated as follows:<br><br> _If the meter name exactly matches.<br>_ If the meter name matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["name","config"]`<br>

### ExperimentalOtlpFileExporter {#experimentalotlpfileexporter}

> **Warning:** This type is experimental and subject to breaking changes.

| Property        | Type                                  | Required? | Default Behavior                    | Description                                                                                                             |
| --------------- | ------------------------------------- | --------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `output_stream` | one of:<br>• `string`<br>• `null`<br> | `false`   | If omitted or null, stdout is used. | Configure output stream. <br>Values include stdout, or scheme+destination. For example: file:///path/to/file.jsonl.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalOtlpFileMetricExporter {#experimentalotlpfilemetricexporter}

> **Warning:** This type is experimental and subject to breaking changes.

| Property                        | Type                                                                          | Required? | Default Behavior                               | Description                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------- | --------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `default_histogram_aggregation` | [`ExporterDefaultHistogramAggregation`](#exporterdefaulthistogramaggregation) | `false`   | If omitted, explicit_bucket_histogram is used. | Configure default histogram aggregation.<br>                                                                            |
| `output_stream`                 | one of:<br>• `string`<br>• `null`<br>                                         | `false`   | If omitted or null, stdout is used.            | Configure output stream. <br>Values include stdout, or scheme+destination. For example: file:///path/to/file.jsonl.<br> |
| `temporality_preference`        | [`ExporterTemporalityPreference`](#exportertemporalitypreference)             | `false`   | If omitted, cumulative is used.                | Configure temporality preference.<br>                                                                                   |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalPeerInstrumentation {#experimentalpeerinstrumentation}

> **Warning:** This type is experimental and subject to breaking changes.

| Property          | Type                                                                           | Required? | Default Behavior                               | Description                                                                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------ | --------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `service_mapping` | `array` of [`ExperimentalPeerServiceMapping`](#experimentalpeerservicemapping) | `false`   | If omitted, no peer service mappings are used. | Configure the service mapping for instrumentations following peer.service semantic conventions.<br>See peer.service semantic conventions: <https://opentelemetry.io/docs/specs/semconv/general/attributes/#general-remote-service-attributes><br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalPeerServiceMapping {#experimentalpeerservicemapping}

> **Warning:** This type is experimental and subject to breaking changes.

| Property  | Type     | Required? | Default Behavior                           | Description                                                    |
| --------- | -------- | --------- | ------------------------------------------ | -------------------------------------------------------------- |
| `peer`    | `string` | `true`    | Property is required and must be non-null. | The IP address to map.<br>                                     |
| `service` | `string` | `true`    | Property is required and must be non-null. | The logical name corresponding to the IP address of .peer.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["peer","service"]`<br>

### ExperimentalProbabilitySampler {#experimentalprobabilitysampler}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                  | Required? | Default Behavior                 | Description          |
| -------- | ------------------------------------- | --------- | -------------------------------- | -------------------- |
| `ratio`  | one of:<br>• `number`<br>• `null`<br> | `false`   | If omitted or null, 1.0 is used. | Configure ratio.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalProcessResourceDetector {#experimentalprocessresourcedetector}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalPrometheusMetricExporter {#experimentalprometheusmetricexporter}

> **Warning:** This type is experimental and subject to breaking changes.

| Property                        | Type                                                                                      | Required? | Default Behavior                                       | Description                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `host`                          | one of:<br>• `string`<br>• `null`<br>                                                     | `false`   | If omitted or null, localhost is used.                 | Configure host.<br>                                                                                                                   |
| `port`                          | one of:<br>• `integer`<br>• `null`<br>                                                    | `false`   | If omitted or null, 9464 is used.                      | Configure port.<br>                                                                                                                   |
| `translation_strategy`          | [`ExperimentalPrometheusTranslationStrategy`](#experimentalprometheustranslationstrategy) | `false`   | If omitted, underscore_escaping_with_suffixes is used. | Configure how metric names are translated to Prometheus metric names.                                                                 |
| `with_resource_constant_labels` | [`IncludeExclude`](#includeexclude)                                                       | `false`   | If omitted, no resource attributes are added.          | Configure Prometheus Exporter to add resource attributes as metrics attributes, where the resource attribute keys match the patterns. |
| `without_scope_info`            | one of:<br>• `boolean`<br>• `null`<br>                                                    | `false`   | If omitted or null, false is used.                     | Configure Prometheus Exporter to produce metrics without a scope info metric.<br>                                                     |
| `without_target_info`           | one of:<br>• `boolean`<br>• `null`<br>                                                    | `false`   | If omitted or null, false is used.                     | Configure Prometheus Exporter to produce metrics without a target info metric for the resource.<br>                                   |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalPrometheusTranslationStrategy {#experimentalprometheustranslationstrategy}

> **Warning:** This type is experimental and subject to breaking changes.

**This is an enum type.**

| Value                                  | Description                                                                                                                               |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `no_translation`                       | Special character escaping is disabled. Type and unit suffixes are disabled. Metric names are unaltered.                                  |
| `no_utf8_escaping_with_suffixes`       | Special character escaping is disabled. Type and unit suffixes are enabled.                                                               |
| `underscore_escaping_with_suffixes`    | Special character escaping is enabled. Type and unit suffixes are enabled.                                                                |
| `underscore_escaping_without_suffixes` | Special character escaping is enabled. Type and unit suffixes are disabled. This represents classic Prometheus metric name compatibility. |

### ExperimentalResourceDetection {#experimentalresourcedetection}

> **Warning:** This type is experimental and subject to breaking changes.

| Property     | Type                                                                       | Required? | Default Behavior                                              | Description                                                                                                                                                           |
| ------------ | -------------------------------------------------------------------------- | --------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `attributes` | [`IncludeExclude`](#includeexclude)                                        | `false`   | If omitted, all attributes from resource detectors are added. | Configure attributes provided by resource detectors.                                                                                                                  |
| `detectors`  | `array` of [`ExperimentalResourceDetector`](#experimentalresourcedetector) | `false`   | If omitted, no resource detectors are enabled.                | Configure resource detectors.<br>Resource detector names are dependent on the SDK language ecosystem. Please consult documentation for each respective language. <br> |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalResourceDetector {#experimentalresourcedetector}

> **Warning:** This type is experimental and subject to breaking changes.

`ExperimentalResourceDetector` is an SDK extension plugin point.

| Property    | Type                                                                              | Required? | Default Behavior    | Description                                                                                                                                |
| ----------- | --------------------------------------------------------------------------------- | --------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `container` | [`ExperimentalContainerResourceDetector`](#experimentalcontainerresourcedetector) | `false`   | If omitted, ignore. | Enable the container resource detector, which populates container.\* attributes.<br>                                                       |
| `host`      | [`ExperimentalHostResourceDetector`](#experimentalhostresourcedetector)           | `false`   | If omitted, ignore. | Enable the host resource detector, which populates host._and os._ attributes.<br>                                                         |
| `process`   | [`ExperimentalProcessResourceDetector`](#experimentalprocessresourcedetector)     | `false`   | If omitted, ignore. | Enable the process resource detector, which populates process.\* attributes.<br>                                                           |
| `service`   | [`ExperimentalServiceResourceDetector`](#experimentalserviceresourcedetector)     | `false`   | If omitted, ignore. | Enable the service detector, which populates service.name based on the OTEL_SERVICE_NAME environment variable and service.instance.id.<br> |

**Constraints:**

• `additionalProperties`: `{"type":["object","null"]}`<br>• `minProperties`:
`1`<br>• `maxProperties`: `1`<br>

### ExperimentalServiceResourceDetector {#experimentalserviceresourcedetector}

> **Warning:** This type is experimental and subject to breaking changes.

**No properties.**

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalSpanParent {#experimentalspanparent}

> **Warning:** This type is experimental and subject to breaking changes.

**This is an enum type.**

| Value    | Description                            |
| -------- | -------------------------------------- |
| `local`  | local, a local parent.                 |
| `none`   | none, no parent, i.e., the trace root. |
| `remote` | remote, a remote parent.               |

### ExperimentalTracerConfig {#experimentaltracerconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property   | Type      | Required? | Default Behavior           | Description                                |
| ---------- | --------- | --------- | -------------------------- | ------------------------------------------ |
| `disabled` | `boolean` | `false`   | If omitted, false is used. | Configure if the tracer is enabled or not. |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalTracerConfigurator {#experimentaltracerconfigurator}

> **Warning:** This type is experimental and subject to breaking changes.

| Property         | Type                                                                                   | Required? | Default Behavior                                                                            | Description                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `default_config` | [`ExperimentalTracerConfig`](#experimentaltracerconfig)                                | `false`   | If omitted, unmatched .tracers use default values as described in ExperimentalTracerConfig. | Configure the default tracer config used there is no matching entry in .tracer_configurator/development.tracers. |
| `tracers`        | `array` of [`ExperimentalTracerMatcherAndConfig`](#experimentaltracermatcherandconfig) | `false`   | If omitted, all tracers use .default_config.                                                | Configure tracers.                                                                                               |

**Constraints:**

• `additionalProperties`: `false`<br>

### ExperimentalTracerMatcherAndConfig {#experimentaltracermatcherandconfig}

> **Warning:** This type is experimental and subject to breaking changes.

| Property | Type                                                    | Required? | Default Behavior                           | Description                                                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------- | --------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config` | [`ExperimentalTracerConfig`](#experimentaltracerconfig) | `true`    | Property is required and must be non-null. | The tracer config.                                                                                                                                                                                                                                               |
| `name`   | `string`                                                | `true`    | Property is required and must be non-null. | Configure tracer names to match, evaluated as follows:<br><br> _If the tracer name exactly matches.<br>_ If the tracer name matches the wildcard pattern, where '?' matches any single character and '\*' matches any number of characters including none.<br> |

**Constraints:**

• `additionalProperties`: `false`<br>• `required`: `["name","config"]`<br>

<!-- END GENERATED: types SOURCE: opentelemetry-configuration -->
