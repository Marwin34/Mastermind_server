import communication
import engine

import time


if __name__ == '__main__':
    game_engine = engine.Engine()
    communication_module = communication.ComSupervisor(game_engine.get_players())
    time_stamp = 0.016  # 60 FPS
    last_update = 0

    print("Server started!")

    while True:
        if time.perf_counter() - last_update >= time_stamp:
            # print(1 / (time.perf_counter() - last_update))
            communication_module.fetch_events()
            game_engine.update()
            communication_module.send()
            game_engine.clean(communication_module)
            last_update = time.perf_counter()
