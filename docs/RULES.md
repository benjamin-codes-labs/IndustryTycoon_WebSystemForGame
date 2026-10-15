# Industry Tycoon — Rulebook

English · [繁體中文](RULES.zh-Hant.md) · [Back to README](../README.md)

> [!IMPORTANT]
> All numbers in this rulebook match the companion app
> ([`catalog.py`](../industry_tycoon/catalog.py) and [`rules.py`](../industry_tycoon/rules.py)),
> which does the bookkeeping during play. If the two ever disagree, the app wins.

## Contents

1. [Premise](#premise)
2. [Components](#components)
3. [Setup](#setup)
4. [Turn structure](#turn-structure)
5. [Combat and the King](#combat-and-the-king)
6. [Winning the game](#winning-the-game)
7. [Economy](#economy)
8. [Inflation](#inflation)
9. [Reference tables](#reference-tables)

## Premise

You run a multinational corporation in a fiercely competitive world. To stand out you must grow
your own business while holding back, and ultimately eliminating, your rivals. The simplest way
to do that is to control resources and use them well.

Move your pieces strategically, seize the land's natural resources, build up industry and
weaken your opponents' companies until they collapse. The last tycoon standing, or the richest
one, wins.

## Components

| Component | Purpose |
|---|---|
| Map tiles (20) | Form the board. Coloured areas are resource points: wood, iron, gold, crude oil, fish, crops, meat, stone, coal and livestock. |
| Character cards | Each character has unique abilities, upkeep and HP (see [Characters](#characters)). |
| Special skill cards | One-shot effects that swing the game (see [Special skill cards](#special-skill-cards)). |
| Building tiles | Collection plants and processing plants placed on the board. |
| Dice (4) | Decide turn order and resolve some abilities. |
| Pieces | King, Queen, General, Castle, Bishop, Knight and Soldier in four colours. |
| Companion app | Tracks money, resources, buildings, pieces and inflation. |

**Players:** 2–4 · **Playing time:** about 20–40 minutes

## Setup

1. Roll dice to choose the **Landowner**, who acts first and plays white. The other players
   take black, blue and red in turn order. Everyone rolls two dice for turn order: the lowest
   total goes first.
2. The Landowner draws two map tiles at random. The referee shuffles every deck separately and
   sets them aside.
3. Each player draws two character cards and keeps one.
4. The Landowner places the map tiles anywhere, with at least three connected squares between
   tiles.
5. In turn order, each player places their base on an empty area. The eight squares around a
   base form its **base area**.
6. Each player starts with one **King**, one **Queen** and one **Soldier** in their base area.
7. Start a new game in the app with the same names, characters and turn order.

## Turn structure

### 1. Preparation

- Collect resources or money. Collection plant output is credited automatically by the app.
- Draw one special skill card if you used one last turn.

### 2. Movement

- Each piece may move **once** per turn.
- Moving onto an enemy piece's square attacks and kills it. Dead pieces cannot return to the
  board.
- A piece that reaches a resource area may build a collection plant there (pay in the app, then
  place the tile).
- Each player may construct **one building per turn**. Processing plants may only be built in
  your base area.
- Pieces bought during the turn are placed in your reserve or base area.

### 3. Card play

- **Insurance.** Pay in the app, then draw an insurance card and place it face up. It protects
  the designated player's buildings and pieces from all damage until the end of the turn,
  except when a protected piece attacks another player's King. Limit one per turn; discard it
  at the start of your next turn.
- **Special skills.** Each card is single-use and discarded after play. You may play any number
  per turn, normally only during your own turn. You may hold at most **your King's HP + 1**
  cards.

### 4. End of turn

Press **下一位玩家** in the app. Play passes to the next player; when everyone has acted, the
round ends.

## Combat and the King

- Attacking an enemy King deals **1 damage** to it. A King with 0 HP dies, which eliminates its
  owner.
- Whatever the result, the attacking piece returns to its own base area.
- Record captured pieces in the app (**擊殺棋子**). Characters with a capture bounty are paid
  automatically.

## Winning the game

The game ends when one of the following happens:

1. **Last tycoon standing.** A player whose King is destroyed is eliminated. When only one
   player remains, they win.
2. **Bankruptcy.** A player who starts **three consecutive turns** with no money is eliminated
   (the app does this automatically).
3. **The deck runs out.** When the special skill deck is exhausted, the game enters
   **overtime**. Each remaining player rolls one die; the highest roller may move or rotate one
   map tile. All special skill cards are reshuffled into the deck. When the deck runs out
   again, finish the round. The player with the most money wins; ties are broken by the number
   of buildings, then by the number of pieces. If players are still tied, the game is a draw.

If the table agrees to stop early, the leaderboard in the app ranks players by net worth.

## Economy

| Rule | Value |
|---|---|
| Starting money | 1,500 |
| Upkeep (paid at the end of each turn) | Character's base upkeep + 10 for every piece bought |
| Minimum balance | Upkeep never takes money below 0 |
| Insurance | 500 (not affected by inflation) |
| Building limit | 15 per player, 28 on the board |
| Processed goods | Delivered when the investing player's turn ends |

**Collection plants** yield their output to their owner at the start of each of the owner's
turns. **Processing plants** turn raw resources into goods. The number of units produced is

```text
units = round( Σ (price of input × quantity) × value multiplier ÷ price of the good )
```

using current market prices. **Net worth**, shown on the leaderboard, is money plus the market
value of all resources and pieces held. A synthesized piece is worth the sum of its components.

## Inflation

At the start of every new round the app re-prices everything: resources, collection plants,
processing plants and pieces. The multiplier is shown in the header as **通貨膨脹率**. The
model measures the average wealth per player and moves prices in proportion to how fast that
wealth is changing.

$$\zeta_n = M + I_{n-1}\sum_{r} w_r k_r + 50B + 100S \qquad P_n = \frac{\zeta_n}{N}$$

$$I_n = 1 + 0.2\, d_n \, \frac{P_n - P_{n-1}}{P_n}$$

| Symbol | Meaning |
|---|---|
| $M$ | Total cash held by all players |
| $k_r$, $w_r$ | Units of raw resource $r$ held by all players, and its inflation weight |
| $B$, $S$ | Buildings on the board and pieces owned, across all players |
| $N$ | Number of players |
| $I_{n-1}$ | The previous round's multiplier (1 before the first adjustment) |
| $d_n$ | $+1$ or $-1$, drawn at random each round |
| $P_{n-1}$ | The previous round's level; for the first adjustment, $0.95\,P_n$ |

Every price is multiplied by $I_n$ and rounded to a whole number. Because of the bootstrap
value, the first adjustment is always exactly ±1%.

## Reference tables

Prices are **base** prices at the start of the game; inflation moves them from round 2
onwards. The app always shows the current price.

### Raw resources

| Resource | App label | Sale price | Output per plant per turn | Collection plant cost | Inflation weight |
|---|---|---:|---:|---:|---:|
| Wood | 木材 | 60 | 3 | 670 | 25 |
| Iron ore | 鐵 | 160 | 2 | 1,200 | 50 |
| Gold | 黃金 | 600 | 1 | 2,400 | 250 |
| Crude oil | 原油 | 400 | 1 | 1,680 | 200 |
| Fish | 魚 | 48 | 3 | 480 | 20 |
| Crops | 農作物 | 40 | 3 | 480 | 20 |
| Meat | 肉 | 46 | 2 | 530 | 20 |
| Stone | 石頭 | 80 | 3 | 864 | 25 |
| Coal | 煤炭 | 120 | 3 | 1,250 | 100 |
| Livestock | 畜牧 | 44 | 3 | 510 | 25 |

### Processed goods

| Good | App label | Sale price | Inputs | Value multiplier | Plant cost | Plant colour |
|---|---|---:|---|---:|---:|---|
| Steel | 鋼鐵 | 840 | Fine iron, coal | ×3 | 2,510 | Purple |
| Fine iron | 精鐵 | 320 | Iron ore | ×2 | 950 | Red |
| Gasoline | 汽油 | 800 | Crude oil (煉油加工廠) | ×2 | 2,300 | Yellow |
| Food | 食物 | 270 | Fish, crops, meat | ×2 | 600 | Green |
| Building material | 建材 | 600 | Wood, stone, fine iron | ×2 | 1,500 | Blue |

### Pieces

| Piece | App label | Price | Synthesized from | Movement |
|---|---|---:|---|---|
| King | 國王 | — | — | One square in any direction |
| Queen | 皇后 | — | Bishop + Castle | Horizontal, vertical or diagonal |
| General | 將軍 | — | Castle + Knight | Horizontal, vertical or L-shape |
| Castle | 城堡 | 660 | — | Horizontal or vertical |
| Bishop | 主教 | 400 | — | Diagonal |
| Knight | 騎士 | 400 | — | L-shape |
| Soldier | 士兵 | 130 | — | One square horizontally or vertically; captures one square in any direction |

### Characters

The **App modifiers** column lists what the app applies automatically. All other abilities are
resolved at the table.

| Character | App label | HP | Base upkeep | Ability | App modifiers |
|---|---|---:|---:|---|---|
| Thomas Edison | 愛迪生 | 2 | 225 | Income is tripled each turn. | Sales ×2, processed output ×1.75 |
| Nikola Tesla | 特斯拉 | 1 | 100 | Draws two special skill cards per turn and may play any non-resource card as Heal. When one of his pieces dies, he names a player who draws a card; if it is a resource card, that player loses 1 HP (Invincible or Heal can negate it). | — |
| Empress Dowager Cixi | 慈禧 | 5 | 0 | Income and resources −30%; factory construction −10%. | Sales ×0.7, plant output ×0.7, construction ×0.9 |
| Nicholas II | 尼古拉斯二世 | 2 | 150 | Buildings take twice as long to construct, but he gains one Soldier each turn and dead pieces may return to the board. | — |
| Yuan Longping | 袁隆平 | 3 | 250 | Output of every industry except mining is doubled, including resources from special skill cards. | Sales ×3 |
| Genghis Khan | 成吉思汗 | 2 | 150 | Moves $x + 2$ times per turn, where $x$ is HP lost; cannot construct buildings; earns 175 per enemy piece killed. | Capture bounty 175 |
| Qin Shi Huang | 秦始皇 | 3 | 250 | Construction and piece costs are halved. | Construction ×0.5, pieces ×0.5 |
| Emperor Meiji | 明治天皇 | 3 | 225 | Income and resources +10%; soldiers can move on water. | — |
| Franklin D. Roosevelt | 羅斯福 | 3 | 175 | May play any special event card as Invincible; income +0.35×. | Sales ×0.5 |
| Liu Xiu | 劉秀 | — | 300 | May buy at most one piece per turn. During card play, reveals cards from the skill deck until a non-resource card appears, keeping every resource card revealed and returning the non-resource card. May discard one enemy soldier per turn. | — |
| J. Robert Oppenheimer | 奧本海默 | — | 170 | If two dice total more than 10, destroys all of one player's pieces except the King and Queen. | Capture bounty 50 |
| Frederick the Great | 腓特烈二世 | — | 400 | If two dice total more than 7, gains one piece of his choice for free (not a General, Queen or King). | — |

### Special skill cards

| Card | Effect |
|---|---|
| Invincible (無懈可擊) | Negates another card's effect. |
| Revolution (革命) | Gain one piece other than a King, Queen or General. |
| Mutual Destruction (玉石俱焚) | If your piece is worth at least as much as an enemy piece, both are destroyed. |
| Heal (回血) | Restore 1 HP to any player's King, even one at 0 HP. Playable at any time, including other players' turns. |
| Guard (守衛) | The chosen King takes no damage until the end of the round. |
| Heavenly Soldiers (天兵) | Summon one piece and place it within the 3×3 area around another player's King. |
| Rebel Invasion (叛軍入侵) | Every piece within a 5×5 area dies. |
| Airdrop (空降) | Teleport one piece anywhere except another player's base area or the 3×3 area around their King. |
| Air Strike (空襲) | Every piece within a 2×5 area dies. |
| Freeze (冰凍) | The next player's soldiers cannot act for one round. |
