import pathlib, sys, os
ROOT_PATH = pathlib.Path(__file__).parents[2]
sys.path.append(os.path.join(ROOT_PATH, 'src'))
print(sys.path)
from operator_precedence_high_roller_bot import high_roller

"""class TestHandleGambleStart(IsolatedAsyncioTestCase):
    async def test_not_gambling_true(self):
        print('HAHAHA')
        await high_roller.handle_gamble_bet(None, None)
        self.assertTrue(True)"""