import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
import random
import ctypes

class BouncingSwitch():
    def __init__(self, dut):
        self.dut = dut

    async def set(self, value, bounce_cycles = 5):
        for x in range(bounce_cycles):
            self.dut.start.value = random.randint(0,1)
            await ClockCycles(self.dut.clk, 1)

        # set the btn value to what it should be
        self.dut.start.value = value
        await ClockCycles(self.dut.clk, 1)

async def reset(dut):
    dut.rst.value = 0
    dut.inv.value = 0
    dut.mode.value = 0
    dut.start.value = 0
    dut.stop.value = 0
    await ClockCycles(dut.clk, 5)

    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)

async def start(dut):
    dut.start.value = 1
    await ClockCycles(dut.clk, 10)

    dut.start.value = 0
    await ClockCycles(dut.clk, 10)

async def mode(dut):
    dut.mode.value = 1
    await ClockCycles(dut.clk, 10)

    dut.mode.value = 0
    await ClockCycles(dut.clk, 10)

async def test_segment_display(dut):
    segment_anode = [
        0b11000000,	 # 0
    	0b11111001,	 # 1
    	0b10100100,	 # 2
    	0b10110000,	 # 3
    	0b10011001,	 # 4
    	0b10010010,	 # 5
    	0b10000010,	 # 6
    	0b11111000,	 # 7
    	0b10000000,	 # 8
    	0b10010000	 # 9
    ]

    await mode(dut)
    await mode(dut)
    await mode(dut)

    count = 0
    while True:
        #assert dut.digit.value == 1 and bin(dut.segment.value) == bin(ctypes.c_uint8(~segment_anode[count]).value), "Mismatch segment cycle value"

        for x in range(4):
            dut._log.info("[timer_counter] segment: %s, digit: %s",
                          dut.segment.value, dut.digit.value)
            await ClockCycles(dut.clk, 1)

        count += 1

        """if count == 5:
            dut.mode.value = 1
            await ClockCycles(dut.clk, 10)
            dut.mode.value = 0
            await ClockCycles(dut.clk, 10)

        if count == 6:
            dut.mode.value = 1
            await ClockCycles(dut.clk, 10)
            dut.mode.value = 0
            await ClockCycles(dut.clk, 10)

        if count == 7:
            dut.start.value = 1
            await ClockCycles(dut.clk, 10)
            dut.start.value = 0
            await ClockCycles(dut.clk, 10)"""

        if count > 9:
            break
        await ClockCycles(dut.clk, 1000)

async def test_start_manual(dut, cycle):
    for x in range(cycle):
        dut._log.info("[timer_counter] clock %s", x)
        await start(dut)
        await ClockCycles(dut.clk, 100)

@cocotb.test()
async def test_timer_counter(dut):
    clock = Clock(dut.clk, 1, "ms")
    await cocotb.start(clock.start())

    clock_per_phase = 10
    switch = BouncingSwitch(dut)
    
    await reset(dut)
    
    """
    # check 1st, 2nd, 3rd, 4th segment digits
    # by waiting for several seconds for display changes
    wait_for = 20
    for x in range(wait_for):
        dut._log.info("[timer_counter] wait about %s", (wait_for-x))
        await ClockCycles(dut.clk, 1000)
    """
    

    """
    for x in range(50):
        #await switch.set(1)
        
        dut._log.info("[timer_counter] segment: %s, digit: %s",
                      dut.segment.value, dut.digit.value)
        await ClockCycles(dut.clk, 1)
    """

    await test_segment_display(dut)
    #await test_start_manual(dut, 128)




