# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/gigagenieM.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/gigagenieM.proto',
  package='kt.gigagenie.ai.m',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x16proto/gigagenieM.proto\x12\x11kt.gigagenie.ai.m\"Y\n\x04reqM\x12\x0f\n\x05voice\x18\x01 \x01(\x0cH\x00\x12\x34\n\ndevCommand\x18\x02 \x01(\x0b\x32\x1e.kt.gigagenie.ai.m.typeCommandH\x00\x42\n\n\x08mRequest\"\x8c\x01\n\x04resM\x12\x0f\n\x05voice\x18\x01 \x01(\x0cH\x00\x12\x34\n\nsrvCommand\x18\x02 \x01(\x0b\x32\x1e.kt.gigagenie.ai.m.typeCommandH\x00\x12\x30\n\x06stream\x18\x03 \x01(\x0b\x32\x1e.kt.gigagenie.ai.m.voiceStreamH\x00\x42\x0b\n\tmResponse\":\n\x0bvoiceStream\x12\x0b\n\x03\x65nd\x18\x01 \x01(\x05\x12\r\n\x05voice\x18\x02 \x01(\x0c\x12\x0f\n\x07\x63hannel\x18\x03 \x01(\x05\"2\n\x0btypeCommand\x12\x0f\n\x07msgType\x18\x01 \x01(\t\x12\x12\n\nmsgPayload\x18\x02 \x01(\t2P\n\nGigagenieM\x12\x42\n\x08serviceM\x12\x17.kt.gigagenie.ai.m.reqM\x1a\x17.kt.gigagenie.ai.m.resM\"\x00(\x01\x30\x01\x62\x06proto3'
)




_REQM = _descriptor.Descriptor(
  name='reqM',
  full_name='kt.gigagenie.ai.m.reqM',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='voice', full_name='kt.gigagenie.ai.m.reqM.voice', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='devCommand', full_name='kt.gigagenie.ai.m.reqM.devCommand', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='mRequest', full_name='kt.gigagenie.ai.m.reqM.mRequest',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=45,
  serialized_end=134,
)


_RESM = _descriptor.Descriptor(
  name='resM',
  full_name='kt.gigagenie.ai.m.resM',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='voice', full_name='kt.gigagenie.ai.m.resM.voice', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='srvCommand', full_name='kt.gigagenie.ai.m.resM.srvCommand', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stream', full_name='kt.gigagenie.ai.m.resM.stream', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='mResponse', full_name='kt.gigagenie.ai.m.resM.mResponse',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=137,
  serialized_end=277,
)


_VOICESTREAM = _descriptor.Descriptor(
  name='voiceStream',
  full_name='kt.gigagenie.ai.m.voiceStream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='end', full_name='kt.gigagenie.ai.m.voiceStream.end', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='voice', full_name='kt.gigagenie.ai.m.voiceStream.voice', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='channel', full_name='kt.gigagenie.ai.m.voiceStream.channel', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=337,
)


_TYPECOMMAND = _descriptor.Descriptor(
  name='typeCommand',
  full_name='kt.gigagenie.ai.m.typeCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgType', full_name='kt.gigagenie.ai.m.typeCommand.msgType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msgPayload', full_name='kt.gigagenie.ai.m.typeCommand.msgPayload', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=339,
  serialized_end=389,
)

_REQM.fields_by_name['devCommand'].message_type = _TYPECOMMAND
_REQM.oneofs_by_name['mRequest'].fields.append(
  _REQM.fields_by_name['voice'])
_REQM.fields_by_name['voice'].containing_oneof = _REQM.oneofs_by_name['mRequest']
_REQM.oneofs_by_name['mRequest'].fields.append(
  _REQM.fields_by_name['devCommand'])
_REQM.fields_by_name['devCommand'].containing_oneof = _REQM.oneofs_by_name['mRequest']
_RESM.fields_by_name['srvCommand'].message_type = _TYPECOMMAND
_RESM.fields_by_name['stream'].message_type = _VOICESTREAM
_RESM.oneofs_by_name['mResponse'].fields.append(
  _RESM.fields_by_name['voice'])
_RESM.fields_by_name['voice'].containing_oneof = _RESM.oneofs_by_name['mResponse']
_RESM.oneofs_by_name['mResponse'].fields.append(
  _RESM.fields_by_name['srvCommand'])
_RESM.fields_by_name['srvCommand'].containing_oneof = _RESM.oneofs_by_name['mResponse']
_RESM.oneofs_by_name['mResponse'].fields.append(
  _RESM.fields_by_name['stream'])
_RESM.fields_by_name['stream'].containing_oneof = _RESM.oneofs_by_name['mResponse']
DESCRIPTOR.message_types_by_name['reqM'] = _REQM
DESCRIPTOR.message_types_by_name['resM'] = _RESM
DESCRIPTOR.message_types_by_name['voiceStream'] = _VOICESTREAM
DESCRIPTOR.message_types_by_name['typeCommand'] = _TYPECOMMAND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

reqM = _reflection.GeneratedProtocolMessageType('reqM', (_message.Message,), {
  'DESCRIPTOR' : _REQM,
  '__module__' : 'proto.gigagenieM_pb2'
  # @@protoc_insertion_point(class_scope:kt.gigagenie.ai.m.reqM)
  })
_sym_db.RegisterMessage(reqM)

resM = _reflection.GeneratedProtocolMessageType('resM', (_message.Message,), {
  'DESCRIPTOR' : _RESM,
  '__module__' : 'proto.gigagenieM_pb2'
  # @@protoc_insertion_point(class_scope:kt.gigagenie.ai.m.resM)
  })
_sym_db.RegisterMessage(resM)

voiceStream = _reflection.GeneratedProtocolMessageType('voiceStream', (_message.Message,), {
  'DESCRIPTOR' : _VOICESTREAM,
  '__module__' : 'proto.gigagenieM_pb2'
  # @@protoc_insertion_point(class_scope:kt.gigagenie.ai.m.voiceStream)
  })
_sym_db.RegisterMessage(voiceStream)

typeCommand = _reflection.GeneratedProtocolMessageType('typeCommand', (_message.Message,), {
  'DESCRIPTOR' : _TYPECOMMAND,
  '__module__' : 'proto.gigagenieM_pb2'
  # @@protoc_insertion_point(class_scope:kt.gigagenie.ai.m.typeCommand)
  })
_sym_db.RegisterMessage(typeCommand)



_GIGAGENIEM = _descriptor.ServiceDescriptor(
  name='GigagenieM',
  full_name='kt.gigagenie.ai.m.GigagenieM',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=391,
  serialized_end=471,
  methods=[
  _descriptor.MethodDescriptor(
    name='serviceM',
    full_name='kt.gigagenie.ai.m.GigagenieM.serviceM',
    index=0,
    containing_service=None,
    input_type=_REQM,
    output_type=_RESM,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_GIGAGENIEM)

DESCRIPTOR.services_by_name['GigagenieM'] = _GIGAGENIEM

# @@protoc_insertion_point(module_scope)