# Copyright (c) 2024，D-Robotics.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import TextSubstitution
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from ament_index_python.packages import get_package_prefix

def generate_launch_description():
    pkg_path = os.path.join(
        get_package_prefix('hobot_bev'),
        "lib/hobot_bev")
    print("hobot_bev path is ", pkg_path)

    # args that can be set from the command line or a default will be used
    config_file_launch_arg = DeclareLaunchArgument(
        "config_file", default_value=TextSubstitution(text=pkg_path+"/config/bev_ipm_base/bev_ipm_base_config.json")
    )
    model_file_launch_arg = DeclareLaunchArgument(
        "model_file", default_value=TextSubstitution(text=pkg_path+"/config/model/model-c359f50c.hbm")
    )
    image_pre_path_launch_arg = DeclareLaunchArgument(
        "image_pre_path", default_value=TextSubstitution(text=pkg_path+"./data/")
    )

    hobot_bev_node = Node(
        package='hobot_bev',
        executable='hobot_bev',
        output='screen',
        parameters=[
            {"pkg_path": pkg_path},
            {"config_file": LaunchConfiguration('config_file')},
            {"model_file": LaunchConfiguration('model_file')},
            {"image_pre_path": LaunchConfiguration('image_pre_path')}
        ],
        arguments=['--ros-args', '--log-level', 'warn']
    )

    hobot_web_node = Node(
        package='websocket',
        executable='websocket',
        output='screen',
        parameters=[
            {"image_topic": "/image_jpeg"},
            {"image_type": "mjpeg"},
            {"only_show_image": True}
        ],
        arguments=['--ros-args', '--log-level', 'warn']
    )
    
    return LaunchDescription([
        config_file_launch_arg,
        model_file_launch_arg,
        image_pre_path_launch_arg,
        hobot_bev_node,
        hobot_web_node
    ])
