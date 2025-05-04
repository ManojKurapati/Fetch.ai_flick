# personal_agent.py
# Simplified: Takes user input for smoking/vaping and triggers habit destroyer flow

from datetime import datetime
from uuid import uuid4
from typing import Literal
import time
import os
import requests
import json
from dotenv import load_dotenv

from uagents import Agent, Context, Model, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement, TextContent, chat_protocol_spec
)
from pydantic.v1 import Field, UUID4

# Load ASI1 config
load_dotenv()
ASI1_MODEL = os.getenv("ASI1_MODEL", "asi1-mini")
ASI1_API_KEY = os.getenv("ASI1_API_KEY")
ASI1_URL = "https://api.asi1.ai/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ASI1_API_KEY}",
}

# TransactAI and HabitDestroyer agent addresses
HABIT_DESTROYER_ADDRESS = "agent1qfat3zdk8c5mmhddhf6y6ras9qqleapmq9k3rka2vpczqwf4wflds238pxk"
TRANSACT_AI_ADDRESS = "agent1qtdvskm3g5ngmvfuqek6shrpjz6ed8jc84s6phmark05z5a8naxawu5jsrq"

# Models
class MetadataContent(Model):
    type: Literal["metadata"] = "metadata"
    metadata: dict[str, str]

class AgentMessage(Model):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    msg_id: UUID4 = Field(default_factory=uuid4)
    content: list[MetadataContent]

class CheckIn(Model):
    hour: int
    did_smoke: bool
    wallet_address: str

# Agent setup
personal_agent = Agent(name="PersonalAgent", seed="personal_agent")
chat_proto = Protocol(spec=chat_protocol_spec)
user_states = {}  # key: sender address, value: state dict

# ASI1 Completion

def get_completion(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are Flick, an AI habit coach."},
        {"role": "user", "content": prompt}
    ]
    payload = {"model": ASI1_MODEL, "messages": messages, "max_tokens": 500}
    try:
        response = requests.post(ASI1_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ASI1 Error] {e}"

@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    state = user_states.setdefault(sender, {
        "wallet": "fetch1testwalletdemoaddressxyz",
        "logs": [],
        "next_prompt": time.time() + 7200
    })

    for item in msg.content:
        if isinstance(item, TextContent):
            text = item.text.strip().lower()
            ctx.logger.info(f"User said: {text}")

            if text in ["yes", "i smoked", "i vaped"]:
                did_smoke = True
                message = "😕 Got it. Logging that. Here's a tip: Replace cravings with deep breathing or cold water."
            elif text in ["no", "i didn't", "nope"]:
                did_smoke = False
                message = "🎉 Amazing! You're winning. Stay on it. Bonus joke: Why don't skeletons smoke? They don't have the guts! 😄"
            else:
                await ctx.send(sender, ChatMessage(
                    timestamp=datetime.utcnow(), msg_id=uuid4(),
                    content=[TextContent(type="text", text="Just type 'yes' or 'no' so I can track you.")]
                ))
                return

            # Send result
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.utcnow(), msg_id=uuid4(),
                content=[TextContent(type="text", text=message)]
            ))

            now = time.localtime()
            state["logs"].append({
                "timestamp": time.time(),
                "hour": now.tm_hour,
                "did_smoke": did_smoke
            })

            await ctx.send(HABIT_DESTROYER_ADDRESS, CheckIn(
                hour=now.tm_hour, did_smoke=did_smoke, wallet_address=state["wallet"]
            ))

            # Visual summary
            lapses = sum(1 for log in state["logs"] if log["did_smoke"])
            streak = sum(1 for log in reversed(state["logs"]) if not log["did_smoke"])
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.utcnow(), msg_id=uuid4(),
                content=[TextContent(type="text", text=f"💰 Escrow: 21 tokens locked\n❌ Lapses: {lapses}\n🔥 Streak: {streak} days")]
            ))

            # ASI1 feedback
            feedback = get_completion(f"User input: '{text}'. Encourage positively.")
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.utcnow(), msg_id=uuid4(),
                content=[TextContent(type="text", text=feedback)]
            ))

            quote = get_completion("Give 1-sentence motivation for quitting smoking.")
            await ctx.send(sender, ChatMessage(
                timestamp=datetime.utcnow(), msg_id=uuid4(),
                content=[TextContent(type="text", text=f"💬 Daily Motivation: {quote}")]
            ))

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"ACK from {sender} for message {msg.acknowledged_msg_id}")

@personal_agent.on_interval(period=300)
async def habit_reminder(ctx: Context):
    now = time.time()
    for user, state in user_states.items():
        if now >= state["next_prompt"]:
            await ctx.send(user, ChatMessage(
                timestamp=datetime.utcnow(), msg_id=uuid4(),
                content=[TextContent(type="text", text="⏰ Quick check-in: Did you smoke or vape in the last 2 hours?")]
            ))
            state["next_prompt"] = now + 7200

personal_agent.include(chat_proto)
