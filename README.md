# ros2_work
По установке:
1) установка ROS2
2) установка PX4-Autopilot (https://github.com/PX4/PX4-Autopilot.git)
3) создаем ros2_ws
далее всё по документации внизу
4) установка xURCE-DDS и px4_msgs (https://docs.px4.io/main/en/ros2/user_guide)
5) создаём свои ноды, пишем управление



прикольный док по ROS2
https://docs.voltbro.ru/starting-ros/messaging/message.html

ctu-mrs.github.io/ros2_obsidian_knowledgebase/main_canvas.html

репозиторий для работы с камерой RPi 
https://github.com/ctu-mrs/libcamera_ros_driver




Установка ultralytics на RPi5 Ubuntu24.04 с ROS2 Jazzy 
1) Пока что я в кривую устанавливаю в глобальный python ultralytics (!!!ОБЯЗАТЕЛЬНО!!!)
ТОЛЬКО С numpy<2
python3 -m pip install --break-system-packages ultralytics "numpy<2"
(пока что это криво, можно делать через виртуальное окружение или через локальную переменную, надо что-то такое думать)
2) Далее получение данных с камеры HQ camera RPi5: 
  2.1) Пока что я установил готовые ноды, которые запускаются через launch
    ros2 launch libcamera_ros_driver camera.launch.py prefix:=front
    Нода публикует данные в топики:
    /uav1/rpi_camera_front/camera_info
    /uav1/rpi_camera_front/camera_raw 
    
    Типы сообщений в топиках: 
    sensor_msgs/msg/CameraInfo
    sensor_msgs/msg/Image
    
    Зная наши топики и типы сообщений пишем собственные ноды
  2.2)  Также пока что я запустил пример с ultralytics-а, чуть позже буду переписывать под свою ноду, тк данные читаются с задержкой
  
  ________________________________________________________________________
  !!!ОБЯЗАТЕЛЬНО!!!
  ВАША МОДЕЛЬ ДОЛЖНА НАХОДИТЬСЯ В ПАПКЕ ROS2_WS ИНАЧЕ COLCON ЕЕ НЕ УВИДЕТ
  ________________________________________________________________________
  
  2.3) Запуск ноды с Hailo8l
