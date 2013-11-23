from frostbite_wire.utils import Packet

packet_attrs = {
    'sequence_number': 100,
    'is_response': True,
    'is_client': False,
    'words': 'this is a test'
}

# What a packet should actually look like on the wire using the attrs above
known_good_packet = u'd\x00\x00@+\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\
this\x00\x02\x00\x00\x00is\x00\x01\x00\x00\x00a\x00\x04\x00\x00\x00test\x00'


def test_packet_word_gettersetters():
    p = Packet(**packet_attrs)
    assert p.words == packet_attrs['words']
    assert p.num_words == len(packet_attrs['words'].split())

    p.words = ''
    assert not p.words
    assert p.num_words == 0

    p.words = packet_attrs['words']
    assert p.words == packet_attrs['words']


def test_packet_sequence_field_gettersetters():
    p = Packet(**packet_attrs)
    assert p.sequence_number == 100
    assert p.is_response is True
    assert p.is_client is False

    p.sequence_number = 123
    assert p.sequence_number == 123
    assert p.is_response is True
    assert p.is_client is False

    p.is_response = False
    assert p.sequence_number == 123
    assert p.is_response is False
    assert p.is_client is False

    p.is_client = True
    assert p.sequence_number == 123
    assert p.is_response is False
    assert p.is_client is True


def test_packet_len():
    # This test also implicitly tests the _size getter and setter
    p = Packet(**packet_attrs)
    # 43 is a preestablished known-good size for
    # the given packet_attrs
    assert len(p) == len(known_good_packet)


def test_packet_bits():
    p = Packet(**packet_attrs)
    assert p.to_buffer() == known_good_packet


def test_packet_coversions():
    p = Packet(**packet_attrs)
    p_copy = Packet.from_buffer(p.to_buffer())

    for attr in packet_attrs:
        assert getattr(p, attr) == getattr(p_copy, attr)

    # Make sure the copied packet's buffer is still mutable/readable
    p_copy.sequence_number = 1000
    assert p_copy.sequence_number == 1000
