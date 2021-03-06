"""runs the command line app for the mailroom as part of lesson 3"""
from pathlib import Path

# setup initial donor list
donors = {'Bill Gates': [100000.00, 5.00, 3000000.00],
          'Paul Allen': [10.00, 1000000.00],
          'Warren Buffet': [300000000.00],
          }

THANK_YOU_DIRECTORY = '/mailroom_thankyou_letters/'

# TODO: refactor to split up process to test
def thank_you(donors=donors):
    """If the user (you) selects ‘Send a Thank You’, prompt for a Full Name.
    If the user types ‘list’, show them a list of the donor names and
    re-prompt.  If the user types a name not in the list, add that name
    to the data structure and use it.  If the user types a name in the
    list, use it.  Once a name has been selected, prompt for a donation
    amount.  Turn the amount into a number – it is OK at this point for
    the program to crash if someone types a bogus amount.
    Once an amount has been given, add that amount to the donation history
    of the selected user.  Finally, use string formatting to compose an
    email thanking the donor for their generous donation. Print the email
    to the terminal and return to the original prompt.
    It is fine (for now) to forget new donors once the script quits running."""

    while True:
        thank_you_input = input('Please select name: ')

        if thank_you_input.lower().strip() == 'list':
            display_donors()
        elif thank_you_input.lower().strip() == 'quit':
            break
        else:
            try:
                donation_amount = float(input("Select donation amount: "))
            except ValueError:
                print('Donation Canceled. Please retry and input number for donation amount.')
            else:
                if thank_you_input not in donors:
                    create_donor(thank_you_input)
                create_donation(fullname=thank_you_input, amount=donation_amount, donors=donors)
                print_thank_you(fullname=thank_you_input, amount=donation_amount, donors=donors)
                break


def display_donors():
    """diplays donors"""
    print("\n".join(list(donors)))


def create_donation(fullname, amount, donors=donors):
    """adds a donation to the donors dict from user input"""
    try:
        donors[fullname].append(amount)
    except KeyError:
        raise KeyError(f'fullname not in donors repository')


def create_donor(fullname, donors=donors):
    """adds new donor to donors"""
    if fullname in donors:
        raise KeyError(f'Name: {fullname} already exists.')
    else:
        donors[fullname] = []


def report():
    """handles process for main screens report selection

    If the user (you) selected “Create a Report”, print a list of your donors,
    sorted by total historical donation amount.
    Include Donor Name, total donated, number of donations and average
    donation amount as values in each row. You do not need to print out all
    their donations, just the summary info.
    Using string formatting, format the output rows as nicely as possible.
    The end result should be tabular (values in each column should align
    with those above and below)
    After printing this report, return to the original prompt.
    At any point, the user should be able to quit their current task and
    return to the original prompt.
    From the original prompt, the user should be able to quit the script
    cleanly.
    Your report should look something like this:
    Donor Name                | Total Given | Num Gifts | Average Gift
    ------------------------------------------------------------------
    William Gates, III         $  653784.49           2  $   326892.24
    Mark Zuckerberg            $   16396.10           3  $     5465.37
    Jeff Bezos                 $     877.33           1  $      877.33
    Paul Allen                 $     708.42           3  $      236.14
    """
    print(f"{'Donor Name':<26}|{'Total Given':^15}|"
          f"{'Num Gifts':^11}|{'Average Gift':^15}")
    print('-'*70)
    donor_stats = [summarize_donor(donor, donors) for donor in donors.keys()]

    donor_stats.sort(key=lambda tup: tup[1], reverse=True)
    for summary in donor_stats:
        print(f"{summary[0]:<26} ${summary[1]:>13.2f}  "
              f"{summary[2]:>10}  ${summary[3]:>14.2f}")


def summarize_donor(donor_name, donors):
    """generates donor summary
    args:
        donor_name: donor name matching key from donors
    returns
        tuple with fields (donor name, total given, num gifts, average gift)"""
    total_given = sum(donors[donor_name])
    num_gifts = len(donors[donor_name])
    average_gift = total_given/num_gifts

    return(donor_name, total_given, num_gifts, average_gift)


def send_letters_to_everyone(donors=donors, thank_you_directory=Path('/mailroom_thankyou_letters')):
    """process to evaluate all donors and create letter to send to
    donors."""
    # iterate through donors and donations to send thank yous
    for donor in donors:
        file_name = "".join([donor.replace(" ", "_").lower(), '.txt'])
        full_path = thank_you_directory / file_name
        print(file_name)
        donor_info = summarize_donor(donor, donors)
        thank_you_text = create_donation_thank_you(fullname=donor,
                                                   amount=donor_info[1])
        try:
            with open(full_path, 'w') as f:
                f.write(thank_you_text)
        except FileNotFoundError:
            print('Mailroom thank you directory not found.  Please create this directory first.')
            break
        else:
            print(f'Thank you letter for {donor} created in "{thank_you_directory}"')


def create_donation_thank_you(fullname, amount):
    """prints thank you message to terminal for donation"""
    return f"""Dear {fullname},

        Thank you for your very kind donation of ${amount:.2f}.

        It will be put to very good use.

                       Sincerely,
                          -The Team"""


def print_thank_you(fullname, amount):
    """prints thank you to console with thank you text"""
    thank_you_text = create_donation_thank_you(fullname, amount)
    print(thank_you_text)


def menu_selection(prompt, dispatch_dict):
    """generic function to create command line menu and route response
    Will continue to ask user for response until valie response is given or
    user quits by entering 0 or quit.
    args:
        prompt: str to be displayed to user
        dispatch_dict: dict which routes user inputs
    """
    while True:
        response = input(prompt)
        if (response == '0') or (response.lower().strip() == 'quit'):
            break
        try:
            dispatch_dict.get(response)()
        except TypeError:
            print('Please enter valid option from list')


if __name__ == '__main__':

    MAIN_MENU_OPTIONS = {'1': thank_you,
                         '2': report,
                         '3': send_letters_to_everyone, }

    user_input = ('Options:\n'
                  '\t1: Create Donation\n'
                  '\t2: Create a Report\n'
                  '\t3: Send letters to everyone\n'
                  '\t0: Quit\n'
                  'Please input number for option: ')

    menu_selection(user_input, MAIN_MENU_OPTIONS)
