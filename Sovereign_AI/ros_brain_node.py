#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time

# IMPORT YOUR CLIENT
# Ensure sovereign_client.py is in the same folder or in your python path
from sovereign_client import SovereignClient

# ==============================================================================
#                               CONFIG SECTION
# ==============================================================================
# The Ngrok URL from your Colab Session
LLM_URL = "https://oldfangled-uniambic-aryanna.ngrok-free.dev"

# The "Job Description" for this specific robot
# Change this string depending on if it's a drone, arm, or rover.
ROBOT_PERSONA = """
You are the High-Level Planner for a ROS 2 Robot.
INPUT: A JSON string describing sensor data and robot state.
OUTPUT: A strictly formatted JSON object with the next high-level command.
SCHEMA: { "action": "string", "parameters": [list], "reasoning": "string" }
Do not use Markdown. Do not include preamble.
"""
# ==============================================================================

class RosBrainNode(Node):
    def __init__(self):
        super().__init__('sovereign_brain_node')
        
        # 1. Initialize the Cloud Brain
        self.brain = SovereignClient(LLM_URL)
        self.brain.set_persona(ROBOT_PERSONA)
        self.get_logger().info("🧠 Sovereign Brain Connected to Cloud.")

        # 2. THE EARS (Subscriber)
        # We listen to a generic topic where other nodes send their status
        # Topic: /brain/input
        # Message Type: String (JSON formatted)
        self.subscription = self.create_subscription(
            String,
            '/brain/input',
            self.listener_callback,
            10
        )

        # 3. THE MOUTH (Publisher)
        # We shout our commands to the rest of the robot
        # Topic: /brain/output
        # Message Type: String (JSON formatted)
        self.publisher_ = self.create_publisher(String, '/brain/output', 10)

        self.get_logger().info("✅ Brain Node Ready. Waiting for input on '/brain/input'...")

    def listener_callback(self, msg):
        """
        Triggered whenever the robot sends a status update.
        """
        sensor_data = msg.data
        self.get_logger().info(f"📥 Received: {sensor_data}")

        # 1. THINK (Send to Colab)
        # We use a low temperature for predictable JSON control
        try:
            ai_response = self.brain.chat(f"Current State: {sensor_data}", temperature=0.1)
            
            # Clean response just in case the AI added markdown
            clean_json = ai_response.replace("```json", "").replace("```", "").strip()
            
            # 2. VALIDATE
            # Ensure it's valid JSON before publishing
            json.loads(clean_json) 

            # 3. ACT (Publish Command)
            cmd_msg = String()
            cmd_msg.data = clean_json
            self.publisher_.publish(cmd_msg)
            self.get_logger().info(f"out -> 📤 Command Published: {clean_json}")

        except json.JSONDecodeError:
            self.get_logger().error(f"❌ AI hallucinated bad JSON: {ai_response}")
        except Exception as e:
            self.get_logger().error(f"❌ System Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = RosBrainNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()