Fetch.ai_flick
AI-powered habit-breaking app using AgentVerse and Transact AI. Users stake funds via escrow; if they stay consistent, funds are sent to Aave/Compound to earn yield. After 20 days, principal + yield is returned. Lapses redirect funds to successful users.

🧠 HabitDestroyer

Break bad habits. Earn yield. Stay accountable.

HabitDestroyer is an AI-powered app built using **AgentVerse** and **Transact AI**, helping users quit harmful habits like smoking or vaping. Users stake funds via an escrow agent; consistency is rewarded with DeFi yield, while lapses forfeit rewards to successful users.

---

🔁 How It Works

1. Stake : User locks funds into a smart escrow via Transact AI.
2. Send : Agent sends the funds to Aave/Compound for 20 days.
3. Track : Users self-report habit lapses via daily prompts.
4. Reward :
   - Success: Principal returned to user.
   - Lapse: Funds redirected to a reward pool for successful users.

---

 ⚙️ Tech Stack

- AgentVerse – modular AI agents to automate logic  
- Transact AI – for money movement & DeFi actions  
- Aave/Compound – to earn interest on escrowed funds  
- Custom Escrow Logic – to manage user commitments  
---

 📦 Example Agent Flow

- `EscrowAgent`: Locks user stake  
- `YieldAgent`: Sends stake to Aave  
- `Scheduler`: Waits 20 days  
- `ValidatorAgent`: Checks behavior logs  
- `ReturnAgent`: Sends funds back or reallocates

---

📅 Coming Soon

- Progress dashboards  
- Habit tracking visualizations  
- Community reward leaderboard  
- Multi-habit support

---

🛠️ Setup

Instructions to deploy and configure agents via AgentVerse.

📡 HabitDestroyer – Usage Guide

This API triggers the HabitDestroyer pipeline built on AgentVerse + Transact AI, which:

Locks a user’s stake in escrow

Sends it to Aave or Compound for yield

Monitors the user's habit behavior

Returns principal

🔐 Authentication
You’ll need an API Key .

Header Example:

Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
📥 Request Body
json
Copy
Edit
{
  "user_id": "u12345",
  "habit": "smoking",
  "stake_amount": 50,
  "wallet_address": "0xYourWalletAddress",
  "escrow_duration_days": 20
}
Field Descriptions:
Field	Type	Description
user_id	string	Unique user identifier
habit	string	The habit user is trying to break (e.g., vaping)
stake_amount	number	Amount staked in USD equivalent
wallet_address	string	User's crypto wallet for returns
escrow_duration_days	number	Number of days to lock funds (default: 20)


🧪 Testing Tips
Use Postman or Insomnia to test the endpoint.

Use AgentVerse’s Playground to simulate and debug flows before deploying to production.



---
🤝 License

Agentverse License. Use, fork, or contribute to help others stay accountable.
