import communication
import engine

import time


if __name__ == '__main__':
    game_engine = engine.Engine()
    communication_module = communication.ComSupervisor("127.0.0.1", 50001, game_engine.get_players())
    time_stamp = 0.016  # 60 FPS
    last_update = 0

    while True:
        if time.perf_counter() - last_update >= time_stamp:
            # print(1 / (time.perf_counter() - last_update))
            communication_module.fetch_events()
            game_engine.update()
            communication_module.send()
            communication_module.clean()
            last_update = time.perf_counter()
