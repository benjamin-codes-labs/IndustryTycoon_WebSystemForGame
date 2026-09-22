# geog-system

# Industry Tycoon — Game Rules & System User Guide (README)

> This is intended for use with the companion website system for the board game **Industry Tycoon**.  
> Purpose: allow players to use the website during the game to quickly calculate and record money, resources, buildings, pieces, inflation, and other game data.

---

## Table of Contents

1. [Background](#background)
2. [Game Components](#game-components)
3. [System Overview](#system-overview)
4. [Game Rules](#game-rules)
   - [Pre-Game Preparation](#pre-game-preparation)
   - [Turn Start](#turn-start)
   - [Preparation Phase](#preparation-phase)
   - [Movement Phase](#movement-phase)
   - [Card Play Phase](#card-play-phase)
   - [End of Action](#end-of-action)
   - [Victory Conditions](#victory-conditions)
   - [Rules for Attacking the King Piece](#rules-for-attacking-the-king-piece)
5. [Inflation Mechanism](#inflation-mechanism)
6. [Special Skill Cards](#special-skill-cards)
7. [Value Reference](#value-reference)
   - [Raw Materials and Their Corresponding Processing Plants](#raw-materials-and-their-corresponding-processing-plants)
   - [Processed Resources and Their Corresponding Processing Plants](#processed-resources-and-their-corresponding-processing-plants)
8. [Characters](#characters)
9. [Pieces](#pieces)
10. [System User Guide](#system-user-guide)
11. [Python Source Files](#python-source-files)

---

## Background

We are now in a highly competitive society. As the boss of a multinational corporation, if you want to stand out among countless enterprises and companies, you must not only strengthen yourself, but also restrict your opponents' development and eliminate them. The simplest and most direct method is to control resources and make good use of them.

Therefore, your task is to use the pieces in your hand, act strategically, occupy and control local natural and human resources, strengthen yourself, and gradually weaken your opponents' companies economically, causing them to collapse or go bankrupt, and ultimately become the richest industry tycoon!

---

## Game Components

- **Number of players**: 2–4
- **Game time**: about 20–40 minutes

### One Set of Map Tiles (20 tiles)

The map directly determines the areas and resources that players' pieces can reach. The map has areas of different colors and patterns, representing different resource points, such as timber, iron, gold, crude oil, fishing, farming, hunting, stone, coal, livestock, etc.

### One Deck of Character Cards

Character cards contain different characters, such as Edison, Tesla, Cixi, Nicholas II, Yuan Longping, Genghis Khan, Qin Shi Huang, Emperor Meiji, Roosevelt, Liu Xiu, Oppenheimer, Frederick the Great, etc.

Each character has unique attributes, including but not limited to: money income bonus, restrictions, and HP.

### One Deck of Special Skill Cards

Special skill cards allow players to activate special effects that directly affect the game and the status of both enemies and allies.

Effects include: Invincible, Revolution, Mutual Destruction, Heal, Guard, Heavenly Soldiers, Rebel Invasion, Airdrop, Air Strike, Freeze, etc.

Each special skill can only be used once. After it is used, the player must draw a new special skill in the next turn.

### One Pack of Building Tiles

Building tiles contain various buildings. Players can use their existing money and resources to construct a building and invest the resources required by that building to obtain processed materials and expand their income.

Constructible building types include steel, iron, crude oil processing plants, food processing plants, building material processing plants, etc.

### Four Dice

Used to determine player action order (the player who rolls the smallest sum with two dice acts first, and the largest sum acts last) and the probability of some special events.

### Resource Points and Resources

Resource points are the way players directly obtain resources (such as money and materials). Players can obtain corresponding resources from resource points, sell resources to get money, or process resources (put them into processing plants) to increase material value, so that players can obtain more money from processed materials.

---

## System Overview

The system is a website mainly used to calculate and record the money income and expenditure that players should have in each turn (such as selling resources, buying buildings, etc.), and to help players complete various actions.

Insurance can be purchased for **$450**, used to protect a designated player's buildings and pieces from any damage (except when the protected side's piece attacks another side's King). The effect only takes effect during the current turn.

---

## Game Rules

### Pre-Game Preparation

- Roll dice to decide who is the Landowner.
- The Landowner randomly draws two map tiles. The judge shuffles all cards separately and places them aside as decks.
- Players randomly draw two character cards, then choose one.
- The Landowner places the map tiles in any area first (there should be at least three connected spaces between map tiles).
- After map placement is complete, place your base on any empty area of the map (the eight spaces around the base are the Base Area).
- Other players place their bases in the previously decided order as their starting positions.
- Each player initially receives one King, one Queen, and one Pawn, and places them in their own Base Area.
- The Landowner is the first player to act. The Landowner's pieces must be white. Other players draw black, blue, and red pieces in order.

---

### Turn Start

#### Preparation Phase

Before each player's turn begins:

- Take resources or money (starting amount is **$1500**; afterward, each turn the player gains money corresponding to their character; see “Characters” for details).
- Draw one special skill card (if a special skill was used in the previous turn).

#### Movement Phase

**Movement**:

- Each piece can move only once per turn.
- If a piece moves to an enemy piece's space, it may attack and kill that enemy piece.
- After a piece dies, it cannot re-enter the board.
- If a piece moves to a resource area, the player may choose whether to build.
- If building, the player must pay the building's construction cost and required materials, and place the building on that space.

**Buying Pieces**:

- Players can use money to buy corresponding pieces.
- After purchase, pieces can be placed in the Reserve Area or within the Base Area.

**Building**:

- If the player has enough money to pay the building's construction cost (payment completed in the system), place the building on the board.
- If the player does not have enough money, the building cannot be constructed.
- Each player can only construct one building per turn.
- There can be at most **7 buildings** on the board.

#### Card Play Phase

**Buying Insurance**:

- After purchasing insurance (payment must be completed in the system), the player draws one card from the insurance deck and places it publicly in front of themselves as this turn's insurance.
- Each player can only buy one insurance per turn and must discard the insurance card in the next turn after purchase.

**Using Special Skills**:

- Special skill cards are one-time use.
- After using a special skill card, the player must discard it.
- There is no limit to the number of special skill cards used per turn.
- Except for exceptions, players can only use special skill cards during their own turn.
- The number of special skill cards that can be stored is limited: storage limit = **own King's HP + 1**.

#### End of Action

The player's action ends, and it is the next player's turn. Repeat the above steps until all players have acted once, then the round ends.

---

### Victory Conditions

The game ends when one of the following situations occurs, and victory is decided:

1. If a player's King piece is destroyed, that player is eliminated. The game continues until only one player remains; that player wins.
2. If a player's money is zero for three rounds, that player is eliminated. The game continues until only one player remains; that player wins.
3. When special skill cards are exhausted, the game enters overtime. If special skill cards are exhausted again, the game ends. The player with the most money after the entire round ends wins. If there is a tie, compare the number of buildings; the player with the most buildings wins. If there is still a tie, compare the number of pieces; the player with the most pieces wins. If there is still a tie, the game is a draw.

**Overtime**:

- The remaining players each roll one die. The player with the highest result may move or rotate the map once.
- Shuffle all special skill cards and return them to the deck; they can be used again.

---

### Rules for Attacking the King Piece

- After attacking an enemy King piece, deduct 1 HP from that King piece.
- If the King's HP reaches zero, it dies.
- Regardless of the result, the piece that attacked the King returns to the Base Area.

---

## Inflation Mechanism

Inflation refers to the phenomenon in which the amount of money in a country or region increases, while the price level also rises accordingly.

If the quantity of a certain resource is greater than a certain value (variable), then the price of that resource will decrease. Conversely, if the quantity of a certain resource is less than a certain value (variable), then the price of that resource will increase.

Let \(P_n\) be the average price level in year \(n\), and \(P_{n-1}\) be the price level in year \(n-1\). The annual inflation rate \(I_n\) can be measured as follows:

- Let \(\zeta\) = total asset value
- Total asset value \(\zeta\) = cash \(M\) + total resource value \(R\) + number of buildings \(B\) + number of pieces \(S\)
- \(R\) = timber + iron + gold + crude oil + fishing + farming + hunting + stone + coal + livestock
- \(R = I_n(25k + 50k + 250k + 200k + 20k + 20k + 20k + 25k + 100k + 25k_n)\)
- where \(k\) is the quantity of each resource
- That is, \(\zeta_n = M + R + 50B + 10S\)
- \(P_n = \zeta_n / 4\)
- Inflation rate \(I_n = 2[(P_n - P_{n-1}) / P_{n-1}](1 + 0.1)\)

> Note: The original formula in the report has OCR ambiguity. The system implementation should be treated as the authoritative version.

---

## Special Skill Cards

| Skill | Effect |
|---|---|
| Revolution | After playing this card, gain one piece other than King, Queen, and General. |
| Mutual Destruction | If the value of your own piece is equal to or higher than the enemy piece, kill both pieces. |
| Heal | Restore 1 HP to a designated player's King. Can be used when a player's HP is 0. Can be used at any time, including during another player's turn. |
| Guard | Before the end of this round, the designated King will not receive any damage. |
| Heavenly Soldiers | After summoning 1 piece, it can be placed within the 3×3 area of another player's King piece. |
| Rebel Invasion | Pieces within a 5×5 area die. |
| Airdrop | A piece can be teleported to any location, but not into another player's Base Area or the 3×3 area of another player's King piece. |
| Air Strike | Kill all pieces within a 2×5 area. |
| Freeze | The next player's soldiers cannot act for one round. |
| Invincible | Listed in the game components. Detailed effect is not given on Pages 10–11. It is used in character/system descriptions as a card that can negate certain effects. |

---

## Value Reference

### Raw Materials and Their Corresponding Processing Plants

> Each building constructed increases the per-turn deduction by **$30**.

| Resource | Sale Price | Per-Turn Generation | Collection Plant Build Price | Collection Plant Color |
|---|---:|---:|---:|---|
| Timber | $60 | 4 | $670 |  |
| Iron Ore | $160 | 3 | $1200 |  |
| Gold | $600 | 2 | $2400 |  |
| Crude Oil | $400 | 2 | $1680 |  |
| Fishing | $48 | 4 | $480 |  |
| Farming | $40 | 4 | $480 |  |
| Hunting | $46 | 4 | $530 |  |
| Stone | $80 | 4 | $864 |  |
| Coal | $120 | 4 | $1250 |  |
| Livestock | $44 | 4 | $510 |  |

---

### Processed Resources and Their Corresponding Processing Plants

> Each processing plant constructed increases the per-turn deduction by **$50**.  
> Processing plants can only be built in the eight spaces around the Base Area (i.e., 3×3 range).

| Processed Resource | Sale Price | Required Resources | Processing Plant Price | Processing Plant Color |
|---|---:|---|---:|---|
| Steel | $840 | Coal + Iron | $2510 | Purple |
| Refined Iron | $320 | Iron | $950 | Red |
| Gasoline | $800 | Crude Oil | $2300 | Yellow |
| Food | $270 | Fish / Vegetables / Livestock | $600 | Green |
| Building Materials | $600 | Timber / Stone / Iron | $1500 | Blue |

---

## Characters

> All characters start with **$1600**.

| Character | Per-Turn Deduction | HP | Skill Description |
|---|---:|---:|---|
| Edison | $120 | 2 | Income is tripled each turn (×3). |
| Tesla | $60 | 1 | Draw two special skill cards per turn; can use any non-resource special skill card as “Heal”; when one of your pieces dies, choose one player to draw one card from the special skill deck. If it is a resource card, that player loses 1 HP (can be negated by “Invincible” or “Heal”). |
| Cixi | $0 | 5 | Income and resources reduced by 30%; factory construction cost -10%. |
| Nicholas II | $80 | 2 | Building construction time is doubled, but each turn gain one Pawn, and dead pieces can re-enter the board. |
| Yuan Longping | $140 | 3 | Resource output of all industries except mining is doubled (including resources gained from special skill cards). |
| Genghis Khan | $80 | 2 | Can move \(x + 2\) times per turn, where \(x\) is lost HP; cannot construct any buildings; each enemy piece killed grants +$175. |
| Qin Shi Huang | $180 | 3 | Building construction cost and soldier acquisition cost are halved. |
| Emperor Meiji | $120 | 3 | Income and resources +10%; soldiers can move on water. |
| Roosevelt | $90 | 3 | Can use any special event card as Invincible; income +0.35×. |
| Liu Xiu | Not shown on Page 18 | Not shown on Page 18 | Can buy at most one piece per turn. During the Card Play Phase, reveal one card from the special skill deck. If it is a resource card, continue drawing until a non-resource card is drawn; that non-resource card is returned to the deck. All resource cards drawn during this process are owned by that player. The card face also says: “Each turn can discard one enemy soldier.” |
| Oppenheimer | Not shown on Page 18 | Not shown on Page 18 | If the sum of two dice is greater than 10, eliminate all soldiers of one player except King and Queen. |
| Frederick the Great | Not shown on Page 18 | Not shown on Page 18 | If the sum of two dice is greater than 7, freely obtain one self-chosen soldier (except General, Queen, and King). |

---

## Pieces

> Each piece owned increases the per-turn deduction by **$10**.

| Piece | Price / Synthesis | Movement |
|---|---|---|
| King | None | Horizontal / Vertical / Diagonal (1 space) |
| Queen | Bishop + Castle | Horizontal / Vertical / Diagonal |
| General | Castle + Knight | Horizontal / Vertical / L-shape |
| Castle | $660 | Horizontal / Vertical |
| Bishop | $400 | Diagonal |
| Knight | $400 | L-shape |
| Soldier / Pawn | $130 | Horizontal / Vertical (1 space); when capturing: Horizontal / Vertical / Diagonal (1 space) |

---

## System User Guide

Because this board game contains many calculations, we created a system that provides players with a platform for calculating and recording money and resources.

For aesthetic reasons, and because the system has many operations, it is recommended to use a tablet, laptop, or other larger electronic device during the game for easier use.

This system can be used by a single judge outside the game for the players, or in the form where players operate it during their turn and then pass the device to the next player, allowing all players to experience operating the system.

Players can choose a mobile phone, tablet, or laptop. After opening the system, when it is that player's turn, pass the device to that player to operate.

### Initialization

Before the first player starts the game, players must go to **InitPage** to define their game name and character.

- Warning: Duplicate names are not allowed.
- Enter Player 1, Player 2, and Player 3 names and characters (character dropdown selection, e.g., Edison).

After that, players must select the **game** page (you must complete the previous step first to avoid system errors).

The game begins, and Player 1 can start operating.

### Main Interface Information

In the lower right corner of the interface, green text is displayed, showing:

- Current player name
- Character
- Resources
- Resource collection and processing
- And each player's “Total Value” (the total value of pieces, resources, and money owned)

### Resource Operations

When a player draws a resource card and needs to take resources, they can go to the first column, find the resource they want to add, and press:

- **“Take (Resource) ×1”** button

This will add one of that resource for the player.

### Building Resource Collection Plants

When a player needs to build a resource collection plant, they can find the corresponding resource in the first column and press:

- **“Build (Resource) Collection Plant”** button

This will deduct money from the player to build the collection plant (if money is insufficient, the action is invalid and nothing happens).

This will cause the player to automatically obtain the corresponding resources in the next round based on the number of collection plants they already have.

### Building Processing Plants

When a player needs to build a processing plant, they can find the corresponding processing plant in the first column and press:

- **“Build (Processed Resource) Processing Plant”** button

This will deduct money from the player to build the processing plant (if money is insufficient, the action is invalid and nothing happens).

### Investing Resources into Processing Plants

When a player needs to invest resources into a processing plant to obtain processed products, they can find in the corresponding processing plant:

- **“Invest (Resource) Quantity”** item

Enter the quantity of resources to invest in the number input area below, then press:

- **“Invest Resources into (Processing Plant)”** button

After completing the action, the player will automatically receive the corresponding quantity of processed products based on the invested resources.

### Selling Resources

If a player wants to sell resources, they can go to the third column, find the resource they want to sell, enter the quantity they want to sell in the number input area, and press:

- **“Sell (Resource)”** button

The system will automatically deduct that resource quantity from the player and increase the player's money according to the price.

### Buying or Synthesizing Pieces

If a player has already purchased or synthesized a piece, they can go to the fourth column, find that piece, and press:

- **“Buy (Piece)”** or **“Synthesize (Piece)”** button

Complete the action. (If the player does not have enough money to buy the piece, nothing will happen.)

### Ending the Turn

If the player has completed all actions, they can go to the fifth column and press:

- **“Next Player”** button

### Eliminating Players

If a player's King has been eliminated, players can go to the fifth column and find that player's:

- **“Eliminate”** option and select it

In the next round, that player will automatically be skipped (if a player goes bankrupt for three consecutive rounds, the system will automatically select it).

### Selling All Resources

If a player wants to sell all resources, they can go to the fifth column and press:

- **“Sell All Resources”** button

Complete the action.

### Destroying Buildings or Pieces

If a player destroys another player's building or piece, they can go to the corresponding input area at the bottom of the fifth column:

- **Target Player**: refers to whose building/piece was destroyed
- **Target Collection Plant** or **Target Piece**: refers to which piece or building was destroyed

Finally press:

- **“Destroy Processing Plant” (Building)** or **“Destroy Piece” (Piece)** button

Complete the action.

### Checking Inflation

Players can go to the bottom area of the **Game** page to check the current inflation rate.

Multiply this number by all values from the previous round to obtain the value of everything in this round.

### Determining the Winner

If players decide not to continue the game, they can look at the green data display area to find which player has the highest value.

The player with the highest value wins.

---

## 11. Python Source Files

The companion website system is implemented with two Streamlit Python files. They share game state through `st.session_state`.

### `1_Init_page.py` — Initialization Page

- This is the first page players should open before starting the game.
- It creates and stores the player names and selected characters in `st.session_state`.
- It provides text inputs for Player 1–4 names and dropdowns for each player’s character:
  - 爱迪生, 特斯拉, 慈禧, 尼古拉斯二世, 袁隆平, 成吉思汗, 秦始皇, 明治天皇, 罗斯福, 刘秀, 奥本海默, 腓特烈二世
- It warns that duplicate names are not allowed.
- It stores:
  - `st.session_state.player_name_list`
  - `st.session_state.char_idx_tuple`
- `game.py` depends on these values. You must complete this page before opening the game page, otherwise the system may error.

### `game.py` — Main Game Page

- This is the main game operation page.
- It uses a wide Streamlit layout and divides the interface into five columns.
- It reads the player names and character choices created by `1_Init_page.py`.
- It initializes and manages most game data in `st.session_state`, including:
  - current round and current player;
  - each player’s money and resources;
  - next-turn resource generation;
  - collection plants and processing plants;
  - owned pieces;
  - building counts;
  - eliminated / bankrupt players;
  - inflation rate and previous inflation value;
  - price mappings for resources, buildings, pieces, and character modifiers.
- It implements the main actions:
  - taking raw resources;
  - building resource collection plants;
  - building processing plants;
  - investing resources into processing plants;
  - selling one resource or all resources;
  - buying or synthesizing pieces;
  - buying insurance;
  - ending the turn / next player;
  - eliminating players;
  - destroying buildings or pieces;
  - checking inflation;
  - displaying current player information and total value.
- It also applies character-specific rules such as income multipliers, building cost reductions, soldier cost reductions, and per-turn deductions.

> Together, `1_Init_page.py` and `game.py` form the companion website system for **Industry Tycoon**.  
> `1_Init_page.py` handles initialization, and `game.py` handles the main game loop and calculations.

---

# 产业大亨 — 游戏规则与系统使用说明（README）


> 本文档根据《地理考试报告》Page 6–22 整理，适用于桌游《资本家的游戏》的配套网站系统。  
> 目的：让玩家在游戏过程中使用网站系统，快速计算金钱、资源、建筑、棋子与通货膨胀等数据。

---

## 目录

1. [背景](#背景)
2. [游戏组成](#游戏组成)
3. [系统概述](#系统概述)
4. [游戏规则](#游戏规则)
   - [游戏前准备](#游戏前准备)
   - [回合开始](#回合开始)
   - [备段](#备段)
   - [移动段](#移动段)
   - [出牌阶段](#出牌阶段)
   - [行动结束](#行动结束)
   - [胜负条件](#胜负条件)
   - [攻击国王棋子相关规则](#攻击国王棋子相关规则)
5. [通货膨胀机制](#通货膨胀机制)
6. [特殊技能牌介绍](#特殊技能牌介绍)
7. [数值查询](#数值查询)
   - [原材料及其对应加工厂](#原材料及其对应加工厂)
   - [加工后资源及其相应加工厂](#加工后资源及其相应加工厂)
8. [角色](#角色)
9. [棋子](#棋子)
10. [系统使用说明](#系统使用说明)
11. [Python 源文件](#python-源文件)

---

## 背景

现在正处于竞争激烈的社会中，作为一名跨国公司的老板，想在数不胜数的企业和公司中脱颖而出，除了壮大自身，还需限制对手的发展，淘汰对手。而最简单、最直接的方法便是控制资源，并善用资源。

因此，你们的任务便是利用手中的棋子，有策略地行动，占据并控制当地的自然资源和人力资源，壮大自身，并在经济层面上逐步削弱对手公司的实力，使其倒闭、破产，最终成为最富有的资本家！

---

## 游戏组成

- **游戏人数**：2–4 人
- **游戏时间**：约 20–40 分钟

### 一副地图块（20 张）

地图直接决定了玩家的棋子可以接触到的地区和资源。地图上面有不同颜色和图案的区域，代表不同的资源点，如木材、铁、黄金、原油、渔业、种植、打猎、石头、煤、畜牧等。

### 一副角色牌

角色牌上面有不同的角色，如爱迪生、特斯拉、慈禧、尼古拉二世、袁隆平、成吉思汗、秦始皇、明治天皇、罗斯福、刘秀、奥本海默、腓特烈二世等。

每一个角色都有着自己独特的属性，包括但不限于：金钱收入加成、限制与血量等。

### 一副特殊技能牌

特殊技能牌使玩家可以自行发动特殊效果，直接影响战局以及敌我双方的状况。

效果包括：无懈可击、革命、玉石俱焚、回血、守卫、天兵、叛军入侵、空降、空袭、冰冻等。

每张特殊技能只可使用一次，当用完以后玩家需在下一个回合抽出新的特殊技能。

### 一包建筑块

建筑牌包含了各式各样的建筑物。玩家可以利用现有的金钱和资源来建造一座建筑物，并投入该建筑物所需的资源，以获得经过加工后的材料，扩大自己的收益。

可建造的建筑物类型包括钢、铁、原油加工厂、食品加工厂、建材加工厂等。

### 四个骰子

用来决定玩家的行动顺序（投出两个骰子和的最小数的玩家为第一个行动的玩家，和最大者为最后一个）和一些特殊事件的发生概率。

### 资源点与资源

资源点是玩家直接获得资源（如：金、材料）的途径。玩家可从资源点获取对应的资源，并可以售卖资源从而获取金，又或者将资源加工（放入加工厂中）来增加材料的价值，这样玩家就可以从加工后的材料中获得更多的钱。

---

## 系统概述

系统是一个网站，主要用于计算和记录玩家在每回合中应有的金收入支出（如：在售卖资源、购买建筑物等），并帮助玩家完成各种行动。

保险可以以 **$450** 购入，用以保护指定玩家的建筑和棋子在任何受到伤害（除了被保护方棋子在攻击其他方的国王时）。效果只在当前回合内生效。

---

## 游戏规则

### 游戏前准备

- 通过骰子决定谁是地主。
- 地主需随机抽取两张地图，裁判将所有牌分别洗牌并放在一边作为牌库。
- 玩家随机抽取两张角色牌，然后自行选择一张。
- 地主先把地图放在任意的区域（地图和地图之间应至少有三格连接）。
- 当地图放置完成，将自己的基地放在地图的任意一个空白区域（围着基地的八格为基地区域）。
- 其他玩家按刚已决定的顺序放置基地作为玩家的起始位置。
- 每位玩家初始获得一个国王、皇后及卒，并分别放在自己的基地区域上。
- 地主是第一位行动的玩家，地主的棋子必须是白色，其他玩家依次抽取黑色、蓝色和红色棋子。

---

### 回合开始

#### 备段

每名玩家开始回合前：

- 拿取资源或金（起始为 **$1500**，随后每回合可获取与角色相应的金，详情可查看「角色」）。
- 抽一张特殊技能牌（若在上回合已使用了特殊技能）。

#### 移动段

**移动**：

- 每个棋子每回合只能移动一次。
- 如果移动到敌方棋子的格子，可以发动攻击，杀死敌方棋子。
- 棋子在死亡后便不能再上场。
- 如果移动到有资源的区域，可以选择是否兴建建筑。
- 如果兴建，需支付该建筑的建造成本以及所需材料，将该建筑放在该格上。

**购买棋子**：

- 玩家可以使用金购买相应的棋子。
- 棋子在购买后可以放在备区，或是基地区范围内。

**建造**：

- 如果该玩家有足够的钱支付该建筑的建造成本（在系统上完成支付），将建筑放在棋盘上。
- 如果该玩家没有足够的钱，则无法建造该建筑。
- 每个玩家每回合只能建造一个建筑。
- 棋盘上最多只能存在 **7 个建筑**。

#### 出牌阶段

**购买保险**：

- 每位玩家在购买保险后（需在系统内完成付款），从保险牌库中抽取一张牌并将其公开放在自己的面前，作为该回合的保险。
- 每个玩家每回合只能购买一个保险，并且需要在购买保险后的下一回合弃置该保险牌。

**使用特殊技能**：

- 特殊技能牌是一次性的。
- 玩家在使用特殊技能牌后需把特殊技能牌弃置。
- 不限每次使用特殊技能牌的数量。
- 除例外，玩家只能在己方回合中使用特殊技能牌。
- 特殊技能牌的储存数量是有限的，储存数量 = **自身国王的血量 + 1**。

#### 行动结束

该玩家的行动结束，轮到下一位玩家行动。重复以上步骤，直到所有玩家都行动了一次，该回合结束。

---

### 胜负条件

游戏结束的条件：当有以下情况发生时，游戏结束，决定胜负：

1. 玩家的国王棋子被消灭后，该玩家被淘汰，游戏继续进行，直到只剩下一位玩家，该玩家胜利。
2. 玩家的金钱为零三局后，该玩家被淘汰，游戏继续进行，直到只剩下一位玩家，该玩家胜利。
3. 特殊技能牌被抽取完毕后，进入加时环节。若特殊技能牌被再次抽取完毕，游戏结束。取该整个回合完结后金钱最多的玩家为胜者；如果有平手，则比较所有玩家的建筑数量，建筑数量最多的玩家为胜者；如果还有平手，则比较所有玩家的棋子数量，棋子数量最多的玩家为胜者；如果还有平手，则该游戏为平局。

**加时**：

- 剩下的玩家需投一次骰子，点数最大者可以移动或旋转一次地图。
- 将所有特殊技能牌洗牌后放回牌库，可重新使用。

---

### 攻击国王棋子相关规则

- 攻击敌方国王棋子后，扣除该国王棋子一点生命值。
- 若国王的生命值为零则死亡。
- 无论如何，攻击国王的棋子都会回到基地区。

---

## 通货膨胀机制

通货膨胀是指一个国家或地区货币数量增加，而同时物价水平也相应上升的现象。

如果某一个资源的数量多于某一个值（变量），那么该资源的价格就会下降。相反，如果某一个资源的数量少于某一个值（变量），那么该资源的价格就会上升。

以 \(P_n\) 为第 \(n\) 年物价平均水准，\(P_{n-1}\) 为第 \(n-1\) 年的物价水准，年度通货膨胀率 \(I_n\) 可测量如下：

- 设 \(\zeta\) = 总资产价值
- 总资产价值 \(\zeta\) = 现金 \(M\) + 资源总价值 \(R\) + 建筑数量 \(B\) + 棋子数量 \(S\)
- \(R\) = 木材 + 铁 + 黄金 + 原油 + 渔业 + 种植 + 打猎 + 石头 + 煤 + 畜牧
- \(R = I_n(25k + 50k + 250k + 200k + 20k + 20k + 20k + 25k + 100k + 25k_n)\)
- 其中 \(k\) 为各资源数量
- 即 \(\zeta_n = M + R + 50B + 10S\)
- \(P_n = \zeta_n / 4\)
- 通货膨胀率 \(I_n = 2[(P_n - P_{n-1}) / P_{n-1}](1 + 0.1)\)

> 注：原文档公式此处存在 OCR 模糊，系统内以实际实现为准。

---

## 特殊技能牌介绍

| 技能 | 效果 |
|---|---|
| 革命 | 打出此牌可获得除国王、皇后和将军以外的一个棋子。 |
| 玉石俱焚 | 在满足己方棋子与敌方棋子的价格一样或更高的前提下，杀死双方的棋子。 |
| 回血 | 回复一点指定玩家的国王的生命值。可在一名玩家血量为 0 的时候对其使用。可以在任何时候使用，包括非己方回合。 |
| 守卫 | 本轮结束前，指定国王不会受到任何伤害。 |
| 天兵 | 可在召唤 1 名棋子后将其放置在除其他玩家的国王棋的三乘三范围内。 |
| 叛军入侵 | 5×5 范围内的棋子死亡。 |
| 空降 | 可将一名棋子传送到任何地方，但不包括其他玩家的基地区以及其他玩家的国王棋的三乘三范围内。 |
| 空袭 | 在 2×5 范围内杀死所有棋子。 |
| 冰冻 | 下一个玩家的士兵在一轮中无法行动。 |
| 无懈可击 | 游戏组成中列出；Page 10–11 未列出详细效果。角色/系统说明中作为可抵消部分效果的牌使用。 |

---

## 数值查询

### 原材料及其对应加工厂

> 每建造一个建筑，每回合的扣除金额增加 **30 元**。

| 资源 | 售卖价格 | 每回合生成数量 | 收集厂建造价格 | 收集厂颜色 |
|---|---:|---:|---:|---|
| 木材 | $60 | 4 | $670 |  |
| 铁矿石 | $160 | 3 | $1200 |  |
| 黄金 | $600 | 2 | $2400 |  |
| 原油 | $400 | 2 | $1680 |  |
| 渔业 | $48 | 4 | $480 |  |
| 种植 | $40 | 4 | $480 |  |
| 打猎 | $46 | 4 | $530 |  |
| 石头 | $80 | 4 | $864 |  |
| 煤 | $120 | 4 | $1250 |  |
| 畜牧 | $44 | 4 | $510 |  |

---

### 加工后资源及其相应加工厂

> 每建造一个加工厂，每回合扣除金额增加 **50 元**。  
> 加工厂只可建造在基地周围八格（即 3×3 范围）。

| 加工后资源 | 售卖价格 | 需投入的资源 | 加工厂价格 | 加工厂颜色 |
|---|---:|---|---:|---|
| 钢 | $840 | 煤炭 + 铁 | $2510 | 紫色 |
| 精铁 | $320 | 铁 | $950 | 红色 |
| 汽油 | $800 | 原油 | $2300 | 黄色 |
| 食物 | $270 | 鱼 / 蔬菜 / 牲畜 | $600 | 绿色 |
| 建材 | $600 | 木材 / 石头 / 铁 | $1500 | 蓝色 |

---

## 角色

> 所有角色的起始金额皆为 **$1600**。

| 角色 | 每回合扣除 | 生命值 | 技能介绍 |
|---|---:|---:|---|
| 爱迪生 | $120 | 2 | 每回合收入增加 2 倍（×3）。 |
| 特斯拉 | $60 | 1 | 每回合可抽取两张特殊技能牌；可以将除资源牌外的特殊技能牌当作“回血”使用；当自己的一名棋子死亡时，可指定一名玩家在特殊技能牌库中抽取一张牌，若牌为资源牌，则该玩家扣除 1 点生命值（可被“无懈可击”或“回血”抵消）。 |
| 慈禧 | $0 | 5 | 收入和资源减少 30%，工厂建设成本减 10%。 |
| 尼古拉二世 | $80 | 2 | 建筑物建造时间加倍，但每回合能获得一只卒，并且已死亡的棋子可重新下场。 |
| 袁隆平 | $140 | 3 | 除矿业外的其他产业获得资源产量翻 2 倍（包括特殊技能牌中得到的资源）。 |
| 成吉思汗 | $80 | 2 | 每回合可移动 \(x + 2\) 次，\(x\) 为损失的生命值；不能建造任何建筑；每杀死一名棋子增加 $175。 |
| 秦始皇 | $180 | 3 | 建筑物建造成本及获取士兵费用减半。 |
| 明治天皇 | $120 | 3 | 收入和资源增加 10%，士兵可在水上移动。 |
| 罗斯福 | $90 | 3 | 可以将任意一张特殊事件牌当作无懈可击使用，收入增加 0.35 倍。 |
| 刘秀 | 页 18 未显示 | 页 18 未显示 | 每回合最多只能购买一个棋子。出牌阶段时，可将特殊技能牌库中的一张牌展示出来，若是特殊技能牌中的资源牌则可继续抽取，直到抽出一张非资源牌，后该张非资源牌需放回牌库中。期间所抽出所有的资源牌均由该玩家所拥有。页 18 卡面另写“每回合可以弃置一个敌方的士兵”。 |
| 奥本海默 | 页 18 未显示 | 页 18 未显示 | 如果两个骰子的点数之和大于 10，则消减一位玩家除国王和皇后外的所有士兵。 |
| 腓特烈大帝 | 页 18 未显示 | 页 18 未显示 | 如果两个骰子的点数之和大于 7，则可以免费获得一个自选士兵（将军、皇后、国王除外）。 |

---

## 棋子

> 每拥有一只棋子，每回合扣除金额增加 **$10**。

| 棋子 | 价格 / 合成途径 | 移动方式 |
|---|---|---|
| 国王 | 无 | 水平 / 垂直 / 斜向（一格） |
| 皇后 | 主教和城堡 | 水平 / 垂直 / 斜向 |
| 将军 | 城堡和骑士 | 水平 / 垂直 / L 型 |
| 城堡 | $660 | 水平 / 垂直 |
| 主教 | $400 | 斜向 |
| 骑士 | $400 | L 型 |
| 士兵 | $130 | 水平 / 垂直（一格）；吃棋时：水平 / 垂直 / 斜向（一格） |

---

## 系统使用说明

由于此桌上游戏包含了较多计算，我们创造了一个系统，为玩家们提供了一个金钱和资源运算和记录的平台。

为了美观着想，加上系统有较多操作方式，因此建议在游戏时用平板电脑或笔记本电脑等较大型的电子设备操作系统，方便使用。

此系统可以是场外的一位裁判单独为玩家使用，或者是以玩家们自己在回合操作完后把设备传给下一位玩家的形式，让所有玩家体验操作系统。

玩家们可以选择一部手机、平板电脑或笔记本电脑，打开系统后，当轮到该位玩家时，将设备传给该玩家操作。

> 图表 1：系统链接（原报告二维码）  
> 图表 2：定义名称和角色

### 初始化

在第一位玩家开始游戏前，玩家们需先到 **InitPage** 定义好自己的游戏名以及角色。

- 警告：不能有重复名称。
- 输入玩家一、玩家二、玩家三的名字和角色（角色下拉选择，如：爱迪生）。

其后，玩家需选择 **game** 页面（必需先完成上一步，避免系统出错）。

游戏开始，玩家一可以开始操作了。

### 主界面信息

在界面右下角可看到绿色的字体，显示着：

- 当前玩家名
- 角色
- 资源
- 资源收集和加工
- 以及每一位玩家所拥有的“总价值”（所拥有棋子、资源及金价值之总和）

### 资源操作

当玩家抽中资源牌而需要拿取资源，便可到第一栏找到自己要加的资源，并按下：

- **“拿取（资源）×1”** 按钮

这会让玩家新增一个该样资源。

### 建造资源收集厂

当玩家需要建造资源收集厂，便可在第一栏里找到对应资源，并按下：

- **“建造（资源）收集厂”** 按钮

这会扣除玩家价钱来建造收集厂（若金钱不足则此动作无效，不会发生任何事情）。

这会使玩家下一轮按照已有收集厂之数量自动获取应有资源。

### 建造加工厂

当玩家需要建造加工厂，便可在第一栏里找到相应加工厂，并按下：

- **“建造（加工后资源）加工厂”** 按钮

这会扣除玩家价钱来建造加工厂（若金钱不足则此动作无效，不会发生任何事情）。

### 投入资源进加工厂

当玩家需要投入资源进加工厂购买加工成品，可在相应加工厂中找到：

- **“投入（资源）数量”** 一项

在下方数字输入区填选想投入的资源数量，最后按下：

- **“投入资源进（加工厂）”** 按钮

完成动作后，玩家会根据所投入资源自动收到相应数量的加工制品。

### 售卖资源

若玩家想售卖资源，可到第三栏找到自己想售卖的资源，在数字填写区填写自己想售卖的资源数量，再按下：

- **“卖（资源）”** 按钮

系统会自动扣除玩家该样资源数量，并根据价格增值玩家金钱。

### 购买或合成棋子

若玩家已购买或合成棋子，可到第四栏找到该棋子的一项，然后按下：

- **“购买（棋子）”** 或 **“合成了（棋子）”（合成）** 按钮

完成动作。（若玩家本身没有足够金钱购买棋子，将不会发生任何事情。）

### 结束回合

若玩家已完成所有动作，便可到第五栏找到并按下：

- **“下一位玩家”** 按钮

### 淘汰玩家

若有玩家的国王被淘汰，玩家可到第五栏找到该玩家：

- **“淘汰”** 的选项并选取

在下一回合便会自动跳过该玩家（若有玩家连续破产三局，便会由系统自动选取）。

### 全部资源售卖

若玩家想售卖所有资源，则可到第五栏按下：

- **“全部资源售卖”** 按钮

完成动作。

### 摧毁建筑或棋子

若玩家摧毁了其他玩家的建筑或棋子，便可到第五栏下方找到相应的填写区：

- **目标玩家**：指摧毁了谁的
- **目标收集厂** 或 **目标棋子**：指摧毁了哪种棋子或建筑

最后按下：

- **“摧毁加工厂”（建筑）** 或 **“摧毁了棋子”（棋子）** 按钮

完成动作。

### 查询通货膨胀

玩家可到 **Game** 页面最下方区域查询当前通货膨胀为多少。

将该数字乘在上一回合的所有价值，便能得出这一轮所有东西的价值。

### 决定胜者

若玩家们决定游戏不再继续下去，便可到绿色资料显示区域查找哪位玩家价值最高。

价值最高者胜。

---

## 11. Python 源文件

配套网站系统由两个 Streamlit Python 文件实现。它们通过 `st.session_state` 共享游戏状态。

### `1_Init_page.py` — 初始化页面

- 这是玩家开始游戏前应首先打开的页面。
- 它用于输入玩家 1–4 的名称、选择角色，并把名称和角色索引保存到 `st.session_state`。
- 它提供玩家 1–4 名称的文本输入框和每个玩家的角色下拉菜单：
  - 爱迪生, 特斯拉, 慈禧, 尼古拉斯二世, 袁隆平, 成吉思汗, 秦始皇, 明治天皇, 罗斯福, 刘秀, 奥本海默, 腓特烈二世
- 它警告不能有重复名称。
- 它保存：
  - `st.session_state.player_name_list`
  - `st.session_state.char_idx_tuple`
- `game.py` 依赖这些值。必须先完成此页面，再进入游戏页面，否则系统可能出错。

### `game.py` — 主游戏页面

- 这是主游戏操作页面。
- 它使用 Streamlit 宽屏布局，并把界面分成五栏。
- 它读取 `1_Init_page.py` 中保存的玩家名称和角色。
- 它初始化并管理 `st.session_state` 中的大部分游戏数据，包括：
  - 当前回合和当前玩家；
  - 每位玩家的金钱和资源；
  - 下一回合的资源生成；
  - 收集厂和加工厂；
  - 拥有的棋子；
  - 建筑数量；
  - 已淘汰/破产玩家；
  - 通货膨胀率和上一回合的通货膨胀值；
  - 资源、建筑、棋子和角色修正的价格映射。
- 它实现主要操作：
  - 拿取原材料；
  - 建造资源收集厂；
  - 建造加工厂；
  - 投入资源进加工厂；
  - 售卖一种资源或全部资源；
  - 购买或合成棋子；
  - 购买保险；
  - 结束回合/下一位玩家；
  - 淘汰玩家；
  - 摧毁建筑或棋子；
  - 查询通货膨胀；
  - 显示当前玩家信息和总价值。
- 它还应用角色特定规则，例如收入倍率、建筑成本减少、士兵成本减少和每回合扣除。

> `1_Init_page.py` 和 `game.py` 共同组成 **产业大亨** 的配套网站系统。  
> `1_Init_page.py` 负责初始化，`game.py` 负责主游戏循环和计算。

---
