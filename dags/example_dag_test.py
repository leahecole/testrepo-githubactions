import unit_testing

def test_dag_import():
    import example_dag
    unit_testing.assert_has_valid_dag(example_dag)