# 🚀 Quick Start Guide

## 30-Second Setup

```bash
# 1. Install everything
./install.sh

# 2. Run analysis (generates optimized flip.gg configs)
./lootbox-calc

# 3. Use interactive designer
./flip-gg-designer
```

**That's it!** You now have optimized lootbox configurations ready for flip.gg.

## 📁 What You Get

After running the tools, check these files:

```
outputs/
├── flip_gg_recommended.json     # $2.50 box, 15% house edge
├── flip_gg_optimized.json       # Mathematically optimized
└── flip_gg_custom_*.json        # Your custom designs
```

## 🎯 For Flip.gg Implementation

### Option 1: Use Recommended Config
1. Open `outputs/flip_gg_optimized.json`
2. Copy the exact probabilities to flip.gg
3. Set cost to $2.50

### Option 2: Design Custom
1. Run `./flip-gg-designer`
2. Choose your cost ($0.50-$4.00)
3. Select house edge strategy
4. Get optimized probabilities

## 📊 Example Output

```json
{
  "name": "Flip.gg Lootbox $2.50 (Optimized)",
  "cost": 2.5,
  "items": [
    {
      "name": "Small Coins",
      "value": 0.2,
      "probability": 0.4748,
      "rarity": "common"
    },
    {
      "name": "Mega Jackpot", 
      "value": 25.0,
      "probability": 0.0291,
      "rarity": "legendary"
    }
  ]
}
```

Use these **exact probabilities** in flip.gg for optimal results!

## 🎲 Key Metrics

Your generated lootboxes will have:
- ✅ **House Edge**: 15-17% (profitable but fair)
- ✅ **Break-even Rate**: 25-30% (good player experience)
- ✅ **Player Rating**: "Good" to "Very Good"
- ✅ **Mathematical Accuracy**: 99%+ validated

## 🔧 Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `./lootbox-calc` | Full analysis | Generates all optimized configs |
| `./flip-gg-designer` | Interactive design | Custom cost/house edge |
| `./lootbox-toolkit quick` | Quick comparison | See cost range options |
| `./batch-analyzer` | Compare multiple | Analyze all your designs |

## 💡 Pro Tips

1. **Start with $2.00-$2.50** - Sweet spot for flip.gg
2. **Use 15-17% house edge** - Balanced profitability
3. **Test with simulations** - Validate before implementing
4. **Save configurations** - Reuse successful designs

## ❓ Need Help?

- **Full docs**: `README.md`
- **Flip.gg guide**: `docs/FLIP_GG_GUIDE.md`
- **All commands**: `make help`
- **Tool help**: `./lootbox-toolkit --help`

**You're ready to create profitable, fair lootboxes for flip.gg!** 🎉
