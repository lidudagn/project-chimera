#!/usr/bin/env python3
"""Test wallet skill with real/simulation mode."""
import asyncio
import os
import sys
sys.path.insert(0, '.')

async def main():
    print("🧪 Testing Wallet Skill")
    print("=" * 50)
    
    from skills.wallet_management import WalletSkill
    
    # Create wallet skill
    wallet = WalletSkill(agent_id="chimera_test_001")
    
    # Show wallet info
    info = wallet.get_wallet_info()
    print(f"1. Wallet Info:")
    print(f"   AgentKit Available: {info['agentkit_available']}")
    print(f"   Mode: {info['mode']}")
    print(f"   Daily Limit: ${info['daily_limit']}")
    
    # Initialize wallet
    print(f"\n2. Initializing wallet...")
    init_result = await wallet.initialize_wallet()
    print(f"   Success: {init_result['success']}")
    print(f"   Address: {init_result.get('address', 'N/A')}")
    print(f"   Mode: {init_result.get('mode', 'N/A')}")
    if 'message' in init_result:
        print(f"   Message: {init_result['message']}")
    
    # Check balance
    print(f"\n3. Checking balance...")
    balance = await wallet.get_balance()
    if balance['success']:
        print(f"   Success: Yes")
        print(f"   Mode: {balance.get('mode', 'N/A')}")
        if 'balances' in balance:
            for asset, amount in balance['balances'].items():
                print(f"   {asset}: {amount}")
        if 'total_usd_value' in balance:
            print(f"   Total USD: ${balance['total_usd_value']:.2f}")
    else:
        print(f"   Error: {balance.get('error', 'Unknown')}")
    
    # Test transfer
    print(f"\n4. Testing transfer...")
    transfer = await wallet.transfer_usdc(
        to_address="0xRecipientTest123",
        amount=25.0,
        memo="Skill test payment"
    )
    
    print(f"   Success: {transfer['success']}")
    print(f"   Mode: {transfer.get('mode', 'N/A')}")
    if transfer['success']:
        print(f"   TX Hash: {transfer.get('transaction_hash', 'N/A')}")
        print(f"   Amount: {transfer.get('amount', 'N/A')} USDC")
    else:
        print(f"   Error: {transfer.get('error', 'Unknown')}")
        if transfer.get('limit_exceeded'):
            print(f"   Reason: Daily limit exceeded")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\n📝 Next steps:")
    print("1. Get CDP API keys from https://cdp.coinbase.com")
    print("2. Create .env file with CDP_API_KEY_NAME and CDP_API_KEY_PRIVATE_KEY")
    print("3. Run test again for real blockchain interaction")

if __name__ == "__main__":
    asyncio.run(main())
