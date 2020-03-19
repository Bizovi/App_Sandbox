import file_sync.sync as snc


def test_file_exists_in_source_but_not_dest():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {}

    expected_actions = [
        ('COPY', 'src/fn1', 'dst/fn1')
    ]


def test_file_renamed_in_source():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {'hash1': 'fn2'}

    expected_actions = [
        ('MOVE', 'dst/fn2', 'dst/fn1')
    ]



