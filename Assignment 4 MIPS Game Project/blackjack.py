import random


cards = [
    '1', '2', '3', '4', '5', '6', '7',
    '8', '9', '10', 'J', 'Q', 'K', 'A'
]

cardValues = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11
}


def calculate_score(hand):
    score = sum(cardValues[card] for card in hand)

    aces = hand.count('A')

    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score


def hit(hand, score):
    newCard = random.choice(cards)
    hand.append(newCard)

    score = calculate_score(hand)

    return hand, score


def stand():
    print("Stand")


def double(hand, score):
    hand, score = hit(hand, score)
    return hand, score


def split(hand, bet):
    if len(hand) != 2 or hand[0] != hand[1]:
        print("You can only split your original pair.")
        return None

    hand1 = [hand[0]]
    hand2 = [hand[1]]

    return hand1, hand2, bet, bet


def is_blackjack(hand):
    tenValueCards = ['10', 'J', 'Q', 'K']

    return (
        len(hand) == 2
        and 'A' in hand
        and any(card in tenValueCards for card in hand)
    )


def dealer_turn(dealerHand):
    dealerScore = calculate_score(dealerHand)

    print("\nDealer reveals the hole card.")
    print("Dealer hand:", dealerHand)
    print("Dealer score:", dealerScore)

    while dealerScore < 17:
        newCard = random.choice(cards)
        dealerHand.append(newCard)
        dealerScore = calculate_score(dealerHand)

        print("Dealer hits:", newCard)
        print("Dealer score:", dealerScore)

    if dealerScore > 21:
        print("Dealer busts!")

    else:
        print("Dealer stands.")

    return dealerHand, dealerScore


def settle_hand(playerHand, playerBet, dealerHand, dealerScore):
    playerScore = calculate_score(playerHand)

    print("\nSettling hand:", playerHand)
    print("Player score:", playerScore)

    # Player busts
    if playerScore > 21:
        print("You lose.")
        return 0

    # Dealer busts
    if dealerScore > 21:
        print("Dealer busts. You win!")
        return playerBet * 2

    playerBlackjack = is_blackjack(playerHand)
    dealerBlackjack = is_blackjack(dealerHand)

    # Both player and dealer have blackjack
    if playerBlackjack and dealerBlackjack:
        print("Both have blackjack. Push.")
        return playerBet

    # Player blackjack
    if playerBlackjack:
        print("Blackjack! Paid 3:2.")
        return playerBet * 2.5

    # Dealer blackjack
    if dealerBlackjack:
        print("Dealer has blackjack. You lose.")
        return 0

    # Player wins
    if playerScore > dealerScore:
        print("You win! Paid 1:1.")
        return playerBet * 2

    # Dealer wins
    if playerScore < dealerScore:
        print("Dealer wins. You lose.")
        return 0

    # Tie
    print("Push. Your bet is returned.")
    return playerBet


def play_hand(hand, bet, playerMoney, can_split=True):
    while True:
        score = calculate_score(hand)

        print("\nCurrent hand:", hand)
        print("Current score:", score)
        print("Current bet:", bet)

        if score > 21:
            print("This hand busted.")
            return [(hand, bet)], playerMoney

        if score == 21:
            print("This hand has 21.")
            return [(hand, bet)], playerMoney

        turn = input(
            "Would you like to hit, stand, double, or split? "
        ).lower()

        if turn == "hit":
            hand, score = hit(hand, score)

        elif turn == "stand":
            stand()
            return [(hand, bet)], playerMoney

        elif turn == "double":
            if len(hand) != 2:
                print("You can only double down on your first two cards.")
                continue

            if playerMoney < bet:
                print("You do not have enough money to double down.")
                continue

            playerMoney -= bet
            bet *= 2

            hand, score = double(hand, score)

            print("Double down complete.")
            print("Final hand:", hand)
            print("Final score:", score)

            return [(hand, bet)], playerMoney

        elif turn == "split":
            if not can_split:
                print("You cannot split this hand again.")
                continue

            if len(hand) != 2 or hand[0] != hand[1]:
                print("You can only split your original pair.")
                continue

            if playerMoney < bet:
                print("You do not have enough money to split.")
                continue

            result = split(hand, bet)

            hand1, hand2, bet1, bet2 = result

            # Pay the second equal bet
            playerMoney -= bet2

            # Each new hand receives one additional card
            hand1, score1 = hit(hand1, 0)
            hand2, score2 = hit(hand2, 0)

            print("\nSplit complete.")
            print("Hand 1:", hand1)
            print("Hand 2:", hand2)

            # Play hand 1
            hands1, playerMoney = play_hand(
                hand1,
                bet1,
                playerMoney,
                can_split=False
            )

            # Play hand 2
            hands2, playerMoney = play_hand(
                hand2,
                bet2,
                playerMoney,
                can_split=False
            )

            return hands1 + hands2, playerMoney

        else:
            print("Invalid choice.")


def main():
    playerMoney = 100
    playerLastBet = 0

    while playerMoney > 0:
        print("\nYour Money:", playerMoney)

        try:
            bet = int(input("Please enter your bet --> "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if bet == 0:
            print("Goodbye!")
            break

        if bet < 0:
            print("Your bet cannot be negative.")
            continue

        if bet < playerLastBet:
            print("Your bet must be at least your previous bet.")
            continue

        if bet > playerMoney:
            print("You do not have enough money.")
            continue

        playerMoney -= bet
        playerLastBet = bet

        # Deal the player's original two cards
        playerHand = [
            random.choice(cards),
            random.choice(cards)
        ]

        # Deal the dealer's two cards
        dealerHand = [
            random.choice(cards),
            random.choice(cards)
        ]

        print("\nDealer shows:", dealerHand[0])
        print("Dealer has one hidden card.")

        print("Your starting hand:", playerHand)
        print("Your starting score:", calculate_score(playerHand))

        # Play the player's hand or hands
        playerHands, playerMoney = play_hand(
            playerHand,
            bet,
            playerMoney
        )

        # Dealer plays after all player hands are finished
        dealerHand, dealerScore = dealer_turn(dealerHand)

        # Settle every player hand
        for hand, handBet in playerHands:
            playerMoney += settle_hand(
                hand,
                handBet,
                dealerHand,
                dealerScore
            )

        print("\nRound complete.")
        print("Your Money:", playerMoney)

    print("\nYou failed!")


main()