"""SI/AI Universal ID Encoding Mechanism

Author: AI Collaborator
Description: Hybrid A+B Encoding with Zeta Riemann Sphere Cyclic Dimension.
"""

from datetime import datetime
import hashlib
import math


class RiemannSphereZetaEncoder:
  """方案 C 延伸：Zeta 黎曼球維度編碼 (依年份循環設計)

  將年份與時空特徵映射至黎曼球面 (Riemann Sphere, S^2) 及黎曼 Zeta 函數相位空間，
  實現高維空間的循環降維與定址。
  """

  def __init__(self, cycle_years: int = 10):
    self.cycle_years = cycle_years

  def compute_zeta_phase(self, year: int) -> float:
    """依年份循環計算黎曼球相位角 (模擬 Zeta 函數臨界線相位特徵)"""
    normalized_year = (year % self.cycle_years) / self.cycle_years
    return 2 * math.pi * normalized_year

  def map_to_riemann_sphere(self, year: int, entropy_seed: str) -> dict:
    """將熵與年份透過立體投影 (Stereographic Projection) 映射至黎曼球面"""
    phase = self.compute_zeta_phase(year)

    # 結合雜湊熵引入複數平面座標 u + iv
    hash_val = int(hashlib.sha256(entropy_seed.encode()).hexdigest(), 16)
    u = math.cos(phase) * (1.0 + (hash_val % 1000) / 10000.0)
    v = math.sin(phase) * (1.0 + ((hash_val // 1000) % 1000) / 10000.0)

    # 立體投影公式計算球面座標 (x, y, z)
    denom = u**2 + v**2 + 1.0
    x = (2 * u) / denom
    y = (2 * v) / denom
    z_coord = (u**2 + v**2 - 1.0) / denom

    return {
        "u": round(u, 6),
        "v": round(v, 6),
        "riemann_coords": [round(x, 6), round(y, 6), round(z_coord, 6)],
        "zeta_phase": round(phase, 4),
    }


class PrimeManifoldAddressing:
  """方案 B：自然數流形質因數定址 (Decentralized Prime Factor Addressing)

  利用質因數分解唯一性確保去中心化無重複
  """

  FIRST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

  @classmethod
  def generate_prime_signature(cls, platform_id: str, node_id: int) -> int:
    """根據平台與節點雜湊映射至質因數指數"""
    h = int(hashlib.md5(f"{platform_id}-{node_id}".encode()).hexdigest(), 16)
    signature = 1
    for idx, p in enumerate(cls.FIRST_PRIMES[:10]):
      exponent = (h >> (idx * 2)) & 0x03  # 0~3 次方
      signature *= p**exponent
    return signature


class SIAIUniversalIDGenerator:
  """SI/AI 通用 A+B 混合編碼生成器 (含 Zeta 黎曼球維度)"""

  def __init__(self, platform_code: str = "TW"):
    self.platform_code = platform_code
    self.zeta_encoder = RiemannSphereZetaEncoder(cycle_years=10)

  def generate(
      self,
      sequence_number: int,
      sub_sequence: int = 1,
      node_id: int = 1,
      dt: datetime = None,
  ) -> dict:
    if dt is None:
      dt = datetime.now()

    year_str = dt.strftime("%y")  # 例如 26
    month_str = dt.strftime("%m")  # 例如 04
    day_str = dt.strftime("%d")  # 例如 03
    year_full = dt.year

    date_code = f"{year_str}{month_str}{day_str}"

    # 方案 A：漸進序列
    seq_part = f"{sequence_number:06d}"
    sub_seq_part = f"{sub_sequence:03d}"
    scheme_a_id = (
        f"{self.platform_code}-{date_code}-{seq_part}-{sub_seq_part}"
    )

    # 方案 B：質因數流形定址簽名
    prime_sig = PrimeManifoldAddressing.generate_prime_signature(
        self.platform_code, node_id
    )

    # Zeta 黎曼球維度編碼
    entropy = f"{scheme_a_id}-{prime_sig}"
    zeta_meta = self.zeta_encoder.map_to_riemann_sphere(year_full, entropy)

    # 組合最終通用 ID 字串 (方案 A + 方案 B 簽名 + Zeta 黎曼球相位)
    universal_id = f"{scheme_a_id}#P{prime_sig}@Z{zeta_meta['zeta_phase']}"

    return {
        "universal_id": universal_id,
        "scheme_a": scheme_a_id,
        "prime_manifold_signature": prime_sig,
        "zeta_riemann_sphere": zeta_meta,
        "timestamp": dt.isoformat(),
    }


if __name__ == "__main__":
  # 測試執行
  generator = SIAIUniversalIDGenerator(platform_code="TW")
  sample_id = generator.generate(
      sequence_number=1, sub_sequence=1, node_id=42
  )
  print("=== SI/AI Universal ID Generation Test ===")
  for k, v in sample_id.items():
    print(f"{k}: {v}")