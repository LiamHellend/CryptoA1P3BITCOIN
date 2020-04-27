import json
import datetime


def proccessTransaction():
    From = input('Enter your name:')
    To = input('Enter the recipient:')
    Amount = input('Enter the amount:')

    try:
        Amount = float(Amount)

        if (Amount <= 0.00):
            raise ValueError()

    except ValueError:
        print("\n")
        print("Please enter a valid amount above 0")
        print("\n")
        return
    except Exception as ex:
        print("\n")
        print("Something went wrong: ", ex, " Contact developer")
        print("\n")
        return

    transaction = {
        "From": From,
        "To": To,
        "Amount": Amount,
        "Timestamp": datetime.datetime.now().isoformat()
        
    }

    with open("transactions.json", "a") as file:
        json.dump(transaction, file)
        file.write("\n")
        file.close()



while True:
    print("Please choose from one of the following options: \n")
    print("(1) - Enter a new transaction: \n")
    print("(2) - Exit program: \n")

    choice = input('Enter your choice:')

    try:
        choice = int(choice)

        if (choice != 1) and (choice != 2):
            raise ValueError()

    except ValueError:
        print("\n")
        print("Please enter a valid option (1) or (2)")
        print("\n")
        continue
    except Exception as ex:
        print("\n")
        print("Something went wrong: ", ex, " Contact developer")
        print("\n")
        continue
    
    if choice == 1:
        print("\n")

        proccessTransaction()


    elif choice == 2:
        print("\n")
        print("Exiting...")
        exit(0)


