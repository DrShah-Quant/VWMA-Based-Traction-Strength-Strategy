
from AlgoAPI import AlgoAPIUtil, AlgoAPI_Backtest
from collections import deque

class AlgoEvent:
    def __init__(self):
        # Store history for VWMA calculation
        self.low_prices = deque(maxlen=20)
        self.volumes = deque(maxlen=20)

        # For traction tracking
        self.current_traction = None  # 'positive' or 'negative'
        self.strength_sum = 0  # running total for current traction phase

    def start(self, mEvt):
        self.evt = AlgoAPI_Backtest.AlgoEvtHandler(self, mEvt)
        self.evt.start()

    def calculate_vwma(self):
        """Calculate VWMA using low prices over the last 20 periods."""
        if len(self.low_prices) < 20:
            return None  # not enough data yet
        total_pv = sum(p * v for p, v in zip(self.low_prices, self.volumes))
        total_v = sum(self.volumes)
        return total_pv / total_v if total_v != 0 else None

    def on_bulkdatafeed(self, isSync, bd, ab):
        for instrument, data in bd.items():
            timestamp = data["timestamp"]
            low_price = data["lowPrice"]
            volume = data["volume"]
            current_price = data["lastPrice"]

            # Update rolling data
            self.low_prices.append(low_price)
            self.volumes.append(volume)

            vwma = self.calculate_vwma()

            if vwma is None:
                # Not enough data to calculate VWMA yet
                continue

            # Determine traction
            if current_price > vwma:
                traction = "positive"
            elif current_price < vwma:
                traction = "negative"
            else:
                traction = self.current_traction  # unchanged if exactly equal

            # Accumulate strength for current traction
            sum_add = current_price * volume
            self.strength_sum += sum_add

            # Check for traction change
            if self.current_traction is None:
                # First time setting traction
                self.current_traction = traction

            elif traction != self.current_traction:
                # Traction switched
                self.evt.consoleLog(
                    f"{timestamp} - TRACTION SWITCH from {self.current_traction} to {traction} at price {current_price:,.2f}"
                )
                self.evt.consoleLog(
                    f"{timestamp} - Final {self.current_traction} strength: {self.strength_sum:,.2f} Added: {sum_add:,.2f}"
                )

                # Reset for new traction phase
                self.current_traction = traction
                self.strength_sum = current_price * volume  # start new sum with current tick

            # Print current strength value
            self.evt.consoleLog(
                f"{timestamp} - {traction.capitalize()} strength: {self.strength_sum:,.2f} Added: {sum_add:,.2f}"
            )

    def on_marketdatafeed(self, md, ab):
        pass

    def on_newsdatafeed(self, nd):
        pass

    def on_weatherdatafeed(self, wd):
        pass

    def on_econsdatafeed(self, ed):
        pass

    def on_corpAnnouncement(self, ca):
        pass

    def on_orderfeed(self, of):
        pass

    def on_dailyPLfeed(self, pl):
        pass

    def on_openPositionfeed(self, op, oo, uo):
        pass

