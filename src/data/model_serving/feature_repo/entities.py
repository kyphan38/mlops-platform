from feast import Entity, ValueType

entity_id = Entity(
  name="id",
  value_type=ValueType.INT64
)

entity_host_id = Entity(
  name="host_id",
  value_type=ValueType.INT64
)
