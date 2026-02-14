#!/usr/bin/env python3
"""
Script to publish 100 test jobs to both ranked and practice queues
"""

import json
import pika
import sys

# RabbitMQ connection settings
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"  # Update this with your RabbitMQ URL
RANKED_QUEUE = "match.queue"      # Update with your actual queue name
PRACTICE_QUEUE = "practice.queue"  # Update with your actual queue name

# Sample code to use in jobs (fill this with your actual code)
SAMPLE_CODE = "from oceanmaster.botbase import BotController\nfrom oceanmaster.templates.flash_scout import FlashScout\nfrom oceanmaster.templates.forager import Forager\nfrom oceanmaster.templates.lurker import Lurker\nfrom oceanmaster.templates.saboteur import Saboteur\n#define your custom bot class here\nclass Custom_Bot_Name(BotController):\n    ABILITIES = []\n\n    #set up the bot with any necessary initializations\n    def __init__(self, ctx):\n        super().__init__(ctx)\n        \n    #master strategy for the bot (to be executed at every tick)\n    def act(self):\n        pass\n\n# define the spawn policy for your bots here (the conditions under which they are spawned)\n#return a list/array of bot spawn specifications\ndef spawn_policy(api):\n    policy = []\n    tick = api.get_tick()\n    it = 0;\n    # ZONE 1\n    # for the first 50 ticks spawn scouts every 5 ticks ->10 scouts\n    if tick < 50 and tick % 5==0:\n        policy.append(FlashScout.spawn(location=it))\n        it = it+1\n    \n    \n    # ZONE 2\n    # spawn a forager every 10 ticks and a saboteur every 15 ticks\n    if tick > 50 and tick<120:\n        if tick%10==0:\n            policy.append(Forager.spawn(location=it))\n            it=it+1\n        if tick%15==0:\n            policy.append(Saboteur.spawn(location=it))\n            it=it+1\n        \n        \n    # ZONE 3\n    # spawn less foragers and more saboteurs\n    if tick > 120 and tick <200 and tick%10 == 0:\n        if tick % 10 ==0:\n            policy.append(Saboteur.spawn(location=it))\n            it=it+1\n            \n        if tick % 20 ==0:\n            policy.append(Forager.spawn(location=it))\n            it=it+1\n        \n    \n    # ZONE 4\n    # Harvest more \n    if tick>200:\n        if tick % 10 == 0:\n            policy.append(Forager.spawn(location=it))\n            it=it+1\n        \n        if tick % 30 == 0:\n            policy.append(Saboteur.spawn(location=it))\n            it=it+1\n            \n    # global lurker policy ->every 30 ticks spawn a lurker\n    \n    if tick%30==0:\n        policy.append(Lurker.spawn(location=it))\n        it=it+1\n    \n    return policy"    

def create_job_payload(job_id):
    """Create a job payload with the specified structure"""
    return {
        "id": job_id,
        "p1": 1,
        "p2": 2,
        "p1_code": SAMPLE_CODE,
        "p2_code": SAMPLE_CODE
    }

def publish_jobs(num_jobs=100):
    """Publish jobs to both queues"""
    try:
        # Parse connection URL and connect
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        # Declare queues (idempotent - safe to call even if they exist)
        channel.queue_declare(queue=RANKED_QUEUE, durable=True)
        channel.queue_declare(queue=PRACTICE_QUEUE, durable=True)
        
        print(f"Publishing {num_jobs} jobs to each queue...")
        
        for i in range(1, num_jobs + 1):
            job_payload = create_job_payload(i)
            message = json.dumps(job_payload)
            
            # Publish to ranked queue
            channel.basic_publish(
                exchange='',
                routing_key=RANKED_QUEUE,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            
            # Publish to practice queue
            channel.basic_publish(
                exchange='',
                routing_key=PRACTICE_QUEUE,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            
            if i % 10 == 0:
                print(f"Published {i} jobs to each queue...")
        
        print(f"\n✓ Successfully published {num_jobs} jobs to {RANKED_QUEUE}")
        print(f"✓ Successfully published {num_jobs} jobs to {PRACTICE_QUEUE}")
        print(f"\nTotal messages: {num_jobs * 2}")
        
        connection.close()
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"✗ Failed to connect to RabbitMQ: {e}", file=sys.stderr)
        print(f"  Make sure RabbitMQ is running and the URL is correct: {RABBITMQ_URL}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # You can pass number of jobs as argument
    num_jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    
    print("=" * 60)
    print(f"RabbitMQ Job Publisher")
    print("=" * 60)
    print(f"URL: {RABBITMQ_URL}")
    print(f"Ranked Queue: {RANKED_QUEUE}")
    print(f"Practice Queue: {PRACTICE_QUEUE}")
    print(f"Jobs per queue: {num_jobs}")
    print("=" * 60)
    print()
    
    publish_jobs(num_jobs)