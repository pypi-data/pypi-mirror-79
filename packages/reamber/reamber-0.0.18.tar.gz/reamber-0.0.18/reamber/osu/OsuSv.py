from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Timed import Timed
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

MIN_SV = 0.01
MAX_SV = 10.0

@dataclass
class OsuSv(OsuTimingPointMeta, Timed):
    multiplier: float = 1.0

    @staticmethod
    def codeToValue(code: float) -> float:
        """ Converts the data in the .osu file to the actual SV Value """
        return -100.0 / code

    @staticmethod
    def valueToCode(value: float) -> float:
        """ Converts the actual SV Value to a writable float in .osu """
        return -100.0 / value

    @staticmethod
    def readString(s: str) -> OsuSv or None:
        """ Reads a single line under the [TimingPoints] Label. This must explicitly be a BPM Point. """
        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 8:
            return None

        this = OsuSv()
        assert sComma[6] == '0', "Unexpected BPM Object in OsuSv."
        this.offset = float(sComma[0])
        this.multiplier = OsuSv.codeToValue(float(sComma[1]))
        this.sampleSet = int(sComma[3])
        this.sampleSetIndex = int(sComma[4])
        this.volume = int(sComma[5])
        this.kiai = int(sComma[7])

        return this

    def writeString(self) -> str:
        """ Exports a .osu writable string """
        return f"{self.offset},{self.valueToCode(self.multiplier)}," \
               f"4,{self.sampleSet}," \
               f"{self.sampleSetIndex},{self.volume},{0},{int(self.kiai)}"
