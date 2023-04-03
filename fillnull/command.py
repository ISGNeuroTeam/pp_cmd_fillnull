import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class FillnullCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Keyword("value", required=False, otl_type=OTLType.TEXT),
            Positional("field-list", required=False, otl_type=OTLType.TEXT, inf=True)
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start fillnull command')
        # that is how you get arguments
        field_list = [x.value for x in self.get_iter("field-list")]
        value = self.get_arg("value").value or 0

        # Make your logic here
        if len(field_list) == 0:
            df = df.fillna(value)
        else:
            for column_name in field_list:
                df[column_name] = df[column_name].fillna(value)

        # Add description of what going on for log progress
        self.log_progress('First part is complete.', stage=1, total_stages=2)
        #
        self.log_progress('Last transformation is complete', stage=2, total_stages=2)

        # Use ordinary logger if you need

        self.logger.debug(f'Command fillnul get first positional argument(s) = {field_list}')
        self.logger.debug(f'Command fillnul get keyword argument = {value}')

        return df
