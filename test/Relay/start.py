from i2crelay import I2CRelayBoard

I2C_BUS = 1
I2C_ADDR = 0x26

i2CRelayBoard = I2CRelayBoard(I2C_BUS, I2C_ADDR)
i2CRelayBoard.switch_all_off()

