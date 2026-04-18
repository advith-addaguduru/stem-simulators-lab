"""
Unit tests for simulators.config module.
"""

from simulators.config import CATALOG, get_stats


class TestCatalogStructure:
    """Test catalog data structure."""

    def test_catalog_is_dict(self):
        """Test CATALOG is a dictionary."""
        assert isinstance(CATALOG, dict)
        assert len(CATALOG) > 0

    def test_catalog_packs_have_required_keys(self):
        """Test each pack has required keys."""
        for pack_name, pack_data in CATALOG.items():
            assert "icon" in pack_data
            assert "desc" in pack_data
            assert "subjects" in pack_data
            assert isinstance(pack_data["subjects"], dict)

    def test_catalog_subjects_have_topics(self):
        """Test subjects contain topic lists."""
        for pack_data in CATALOG.values():
            for subject_name, topics in pack_data["subjects"].items():
                assert isinstance(topics, list)
                assert len(topics) > 0

    def test_catalog_topics_have_required_keys(self):
        """Test each topic has required keys."""
        required_keys = ["name", "icon", "desc", "module", "func"]
        for pack_data in CATALOG.values():
            for topics in pack_data["subjects"].values():
                for topic in topics:
                    for key in required_keys:
                        assert key in topic, f"Topic {topic.get('name', 'unknown')} missing {key}"
                    assert isinstance(topic["module"], str)
                    assert isinstance(topic["func"], str)


class TestGetStats:
    """Test get_stats function."""

    def test_get_stats_returns_dict(self):
        """Test get_stats returns a dictionary."""
        stats = get_stats()
        assert isinstance(stats, dict)

    def test_get_stats_has_required_keys(self):
        """Test get_stats has required keys."""
        stats = get_stats()
        required_keys = ["packs", "subjects", "simulators"]
        for key in required_keys:
            assert key in stats
            assert isinstance(stats[key], int)
            assert stats[key] > 0

    def test_get_stats_values_make_sense(self):
        """Test get_stats values are reasonable."""
        stats = get_stats()
        # Should have at least 4 packs (Foundation, Core STEM, Advanced, Cross-Disciplinary)
        assert stats["packs"] >= 4
        # Should have at least 3 subjects (Physics, Chemistry, Mathematics)
        assert stats["subjects"] >= 3
        # Should have many simulators
        assert stats["simulators"] >= 10

    def test_get_stats_calculates_correctly(self):
        """Test get_stats calculation logic."""
        stats = get_stats()

        # Manually calculate expected values
        expected_packs = len(CATALOG)
        expected_subjects = set()
        expected_simulators = 0

        for pack_data in CATALOG.values():
            for subj, topics in pack_data["subjects"].items():
                expected_subjects.add(subj)
                expected_simulators += len(topics)

        assert stats["packs"] == expected_packs
        assert stats["subjects"] == len(expected_subjects)
        assert stats["simulators"] == expected_simulators


class TestCatalogContent:
    """Test catalog content validity."""

    def test_pack_names_are_unique(self):
        """Test pack names are unique."""
        pack_names = list(CATALOG.keys())
        assert len(pack_names) == len(set(pack_names))

    def test_subject_names_are_reasonable(self):
        """Test subject names contain expected subjects."""
        all_subjects = set()
        for pack_data in CATALOG.values():
            all_subjects.update(pack_data["subjects"].keys())

        expected_subjects = {"🔬 Physics", "⚗️ Chemistry", "📐 Mathematics"}
        # Should contain at least the core subjects
        assert expected_subjects.issubset(all_subjects)

    def test_module_paths_exist(self):
        """Test module paths follow expected pattern."""
        for pack_data in CATALOG.values():
            for topics in pack_data["subjects"].values():
                for topic in topics:
                    module_path = topic["module"]
                    assert module_path.startswith("simulators.")
                    # Should have at least 2 dots (simulators.subject.module)
                    assert module_path.count(".") >= 2

    def test_function_names_are_valid(self):
        """Test function names are reasonable."""
        valid_funcs = [
            "simulate", "run", "main", "sim_kinematics_dynamics", "sim_projectile",
            "sim_dc_circuits", "sim_deformation_solids", "sim_forces_density_pressure",
            "sim_waves_superposition", "simulate_equilibrium", "simulate_rate_reaction",
            "simulate_thermochemistry"
        ]
        for pack_data in CATALOG.values():
            for topics in pack_data["subjects"].values():
                for topic in topics:
                    func_name = topic["func"]
                    assert func_name in valid_funcs, f"Unexpected function name: {func_name}"