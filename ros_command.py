#!/usr/bin/env python3

import os
import json
from typing import Dict, Any, Optional

os.environ.setdefault('ROS_MASTER_URI', 'http://192.168.42.78:11311')
os.environ.setdefault('ROS_IP', '192.168.42.88')

try:
    import rospy
    from std_msgs.msg import String
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False
    print("Warning: ROS not available. Install with: source /opt/ros/noetic/setup.bash")


class ROSCommander:
    
    def __init__(self, node_name: str = "cpu_commander"):
        self.node_name = node_name
        self.publisher = None
        self.initialized = False
        
        if not ROS_AVAILABLE:
            print("Warning: ROS not available, commands will not be sent")
            return
        
        try:
            if not rospy.core.is_initialized():
                rospy.init_node(node_name, anonymous=True, disable_signals=True)
            
            self.publisher = rospy.Publisher('/dogu/command', String, queue_size=10)
            
            rospy.sleep(0.5)
            
            self.initialized = True
            print(f"ROSCommander: Connected to {os.environ.get('ROS_MASTER_URI')}")
        except Exception as e:
            print(f"Warning: Failed to initialize ROS: {e}")
            self.initialized = False
    
    def send_command(self, command: str) -> bool:
        if not self.initialized or not self.publisher:
            print(f"Warning: ROS not initialized, cannot send: {command}")
            return False
        
        try:
            msg = String()
            msg.data = command
            self.publisher.publish(msg)
            print(f"ROSCommander: Sent command '{command}'")
            return True
        except Exception as e:
            print(f"Error: Failed to send command: {e}")
            return False
    
    def send_json_command(self, command: Dict[str, Any]) -> bool:
        return self.send_command(json.dumps(command))
    
    def navigate_to(self, target: str) -> bool:
        return self.send_json_command({"type": "navigate", "target": target})
    
    def move_to_user(self) -> bool:
        return self.send_json_command({"type": "move_to_user"})
    
    def stop(self) -> bool:
        return self.send_json_command({"type": "stop"})


_commander = None

def get_commander() -> ROSCommander:
    global _commander
    if _commander is None:
        _commander = ROSCommander()
    return _commander

def send_command(command: str) -> bool:
    return get_commander().send_command(command)

def send_json_command(command: Dict[str, Any]) -> bool:
    return get_commander().send_json_command(command)

def navigate_to(target: str) -> bool:
    return get_commander().navigate_to(target)

def move_to_user() -> bool:
    return get_commander().move_to_user()

def stop() -> bool:
    return get_commander().stop()


if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("ROS Command Sender Test")
    print(f"ROS_MASTER_URI: {os.environ.get('ROS_MASTER_URI')}")
    print(f"ROS_IP: {os.environ.get('ROS_IP')}")
    print("=" * 50)
    
    commander = ROSCommander()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("W") or arg.startswith("w"):
            commander.navigate_to(arg.upper())
        else:
            commander.send_command(arg)
    else:
        print("\nCommands:")
        print("  W1, W2, W3... - Navigate to waypoint")
        print("  move_to_user  - Robot comes to user")
        print("  stop          - Stop robot")
        print("  quit          - Exit\n")
        
        while True:
            try:
                cmd = input("Command: ").strip()
                if cmd.lower() in ('quit', 'exit', 'q'):
                    break
                if not cmd:
                    continue
                    
                if cmd.upper().startswith("W"):
                    commander.navigate_to(cmd.upper())
                elif cmd.lower() == "move_to_user":
                    commander.move_to_user()
                elif cmd.lower() == "stop":
                    commander.stop()
                else:
                    commander.send_command(cmd)
            except (KeyboardInterrupt, EOFError):
                break
        
        print("\nGoodbye!")
