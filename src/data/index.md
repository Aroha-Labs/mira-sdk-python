In an ideal world, everything works as intended and there are no disputes. But that’s not a realistic world view to hold. Especially for optimistic rollups.

In centralized institutions, a single entity holds all the decision-making power, determining what is right and which direction to take. This concentration of authority leaves little room for other users or stakeholders to present their interests or versions of the truth.

Conversely, in decentralized systems like blockchains, there is no single source of truth. Instead, the truth emerges from the consensus of multiple entities within a system that is permissionless to participate in. This structure allows for diverse perspectives but can also lead to disputes when different entities have varying versions of the truth. And this necessitates dispute resolution mechanisms.

Arbitrum’s BoLD

Bounded Liquidity Delay, or BoLD, is Arbitrum’s new dispute resolution mechanism. This protocol is designed to be resistant to attack vectors such as delay attacks, resource exhaustion attacks, and censorship attacks. BoLD is permissionless compared to Arbitrum’s currently deployed dispute resolution protocol. Other optimistic rollups, such as Optimism, Cartesi, and Fuel, have also developed their own dispute-resolution methods.

The Dispute
Before we dive into the different dispute resolution mechanisms, let’s clarify a few things. Let’s have a look at where or when a dispute resolution mechanism enters the picture in an optimistic rollup. When funds are withdrawn from an optimistic rollup back to Ethereum using a roll-up bridge, funds are not immediately credited to your account. Why is this the case?

Optimistic rollups exist so that the L1, Ethereum, does not have to do the compute-heavy job of executing transactions. They optimistically accept L2 state outputs unless those outputs are challenged. Claims are assertions about the state of the L2 given a set of inputs.

Now, the claims aren’t considered valid immediately. They must first pass through a challenge period, which usually lasts 7 days. During this challenge period, each claim can be challenged by a challenger who can contest that a claim is invalid. Now, what we have here is a dispute between those who consider a particular claim valid and those who consider that claim invalid.
