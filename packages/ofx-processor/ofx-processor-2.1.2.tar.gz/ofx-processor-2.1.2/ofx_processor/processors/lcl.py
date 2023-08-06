import sys
from datetime import datetime

import click
import dateparser

from ofx_processor.utils.base_ofx import OfxBaseLine, OfxBaseProcessor


class LclLine(OfxBaseLine):
    def _extract_payee_and_date(self):
        default_date = (
            self.data.dtposted.isoformat().split("T")[0] if self.data.dtposted else None
        )

        if self.data.trntype.lower() == "check":
            return "CHQ", default_date

        if not self.data.name:
            return "", default_date

        split = self.data.name.split()
        if not split:
            return "", default_date

        date_spot = split[-1]
        if "/" not in date_spot:
            return " ".join(split), default_date

        date = dateparser.parse(
            split[-1], date_formats=["%d/%m/%Y"], languages=["fr"]
        )  # type: datetime
        if date:
            name = " ".join(split[:-1])
            date = date.strftime("%Y-%m-%d")  # type: str
        else:
            name = " ".join(split)
            date = default_date

        return name, date

    def get_payee(self):
        return self._extract_payee_and_date()[0]

    def get_date(self):
        return self._extract_payee_and_date()[1]

    def get_memo(self):
        if self.data.trntype.lower() == "check":
            return f"CHQ {self.data.checknum}"
        return super().get_memo()


class LclProcessor(OfxBaseProcessor):
    line_class = LclLine
    account_name = "lcl"
    command_name = "lcl"

    def parse_file(self):
        # The first line of this file needs to be removed.
        # It contains something that is not part of the header of an OFX file.
        try:
            with open(self.filename, "r") as user_file:
                data = user_file.read().splitlines(True)
        except FileNotFoundError:
            click.secho("Couldn't find ofx file", fg="red")
            sys.exit(1)

        if "Content-Type:" in data[0]:
            with open(self.filename, "w") as temp_file:
                temp_file.writelines(data[1:])

        transactions = super(LclProcessor, self).parse_file()

        if "Content-Type:" in data[0]:
            with open(self.filename, "w") as temp_file:
                temp_file.writelines(data)

        return transactions


def main(filename, keep):
    """Import LCL bank statement (OFX file)."""
    LclProcessor(filename).push_to_ynab(keep)
