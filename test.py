from colorama import Fore, Back, Style

from colorama import Fore, Back, Style

def prepate_console_output(counter_number, title, price, currency, search_keyword):
    output_title = ""
    title = title.upper()
    currency = currency.upper()
    search_keyword = search_keyword.upper()
    if search_keyword in title:
        start_pos = title.index(search_keyword)
        end_pos = start_pos + len(search_keyword)
        output_title = (
            f"{Fore.CYAN}{counter_number}"
            f"{Fore.WHITE}: "
            f"{Fore.WHITE}{title[:start_pos]}"
            f"{Fore.CYAN}{title[start_pos:end_pos]}"
            f"{Fore.WHITE}{title[end_pos:]} "
            f"{Fore.WHITE}{price}"
            f"{Fore.YELLOW}{currency}"
        )
    else:
        output_title = (
            f"{Fore.CYAN}{counter_number}"
            f"{Fore.WHITE}: "
            f"{Fore.WHITE}{title} "
            f"{Fore.WHITE}{price}"
            f"{Fore.YELLOW}{currency}"
        )
    return output_title

res = prepate_console_output(2, 'hi hello world', 12, 'azn', 'hhh')
print(res)