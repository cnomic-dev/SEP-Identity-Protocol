"""SI/AI Universal ID Generator - Unit Tests & Distributed Node Verification
File: tests/test_generator.py
"""

from datetime import datetime, timedelta
import unittest
import sys
import os

# 將上一級目錄加入路徑以利匯入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from si_ai_id_generator import SIAIUniversalIDGenerator, PrimeManifoldAddressing, RiemannSphereZetaEncoder


class TestSIAIUniversalIDGenerator(unittest.TestCase):
    """SI/AI 通用 ID 生成器單元測試"""

    def setUp(self):
        self.generator = SIAIUniversalIDGenerator(platform_code="TW")

    def test_scheme_a_formatting(self):
        """測試方案 A 漸進序列格式是否符合規範"""
        fixed_time = datetime(2026, 4, 3, 12, 0, 0)
        res = self.generator.generate(sequence_number=1, sub_sequence=1, dt=fixed_time)
        self.assertEqual(res["scheme_a"], "TW-260403-000001-001")

    def test_prime_manifold_uniqueness(self):
        """測試方案 B 質因數流形簽名的確定性與散列唯一性"""
        sig1 = PrimeManifoldAddressing.generate_prime_signature("TW", node_id=101)
        sig2 = PrimeManifoldAddressing.generate_prime_signature("TW", node_id=101)
        sig3 = PrimeManifoldAddressing.generate_prime_signature("TW", node_id=102)

        self.assertEqual(sig1, sig2, "相同平台與節點應生成相同的質因數簽名")
        self.assertNotEqual(sig1, sig3, "不同節點應生成相異的質因數簽名")

    def test_zeta_riemann_sphere_cycle(self):
        """測試 Zeta 黎曼球 10 年週期循環設計"""
        encoder = RiemannSphereZetaEncoder(cycle_years=10)
        phase_2026 = encoder.compute_zeta_phase(2026)
        phase_2036 = encoder.compute_zeta_phase(2036)

        # 10 年後 Phase 角度應完全相等 (2 * pi * N mod 2 * pi)
        self.assertAlmostEqual(phase_2026, phase_2036, places=5, msg="Zeta 維度編碼應符合 10 年循環週期")

    def test_collision_resistance_high_volume(self):
        """高併發測試：驗證連續生成 10,000 個 ID 無重複"""
        generated_ids = set()
        dt_now = datetime.now()
        for seq in range(1, 10001):
            res = self.generator.generate(sequence_number=seq, node_id=seq % 5, dt=dt_now)
            uid = res["universal_id"]
            self.assertNotIn(uid, generated_ids, f"偵測到 ID 碰撞: {uid}")
            generated_ids.add(uid)

    def test_distributed_node_verification(self):
        """分散式節點 cross-node 驗證機制測試"""
        # 模擬兩個獨立節點 (TW-Node-01 與 TW-Node-02) 於同一秒生成 ID
        dt_shared = datetime(2026, 10, 31, 1, 0, 0)
        res_node1 = self.generator.generate(sequence_number=100, node_id=1, dt=dt_shared)
        res_node2 = self.generator.generate(sequence_number=100, node_id=2, dt=dt_shared)

        # 漸進序列可能相同，但因質因數簽名不同，Universal ID 必須完全不同
        self.assertEqual(res_node1["scheme_a"], res_node2["scheme_a"])
        self.assertNotEqual(res_node1["prime_manifold_signature"], res_node2["prime_manifold_signature"])
        self.assertNotEqual(res_node1["universal_id"], res_node2["universal_id"])


if __name__ == "__main__":
    unittest.main()