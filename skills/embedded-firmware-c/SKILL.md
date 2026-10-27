---
name: embedded-firmware-c
description: Embedded C and firmware engineering for ARM Cortex-M microcontrollers, FreeRTOS task scheduling, hardware register manipulation, SPI/I2C/UART protocols, and deterministic low-power design.
---

# Embedded Systems & ARM Cortex-M Firmware Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Embedded Systems & Hardware Engineering
- **Target Roles**: Embedded Systems and Firmware Engineer, IoT Systems Architect, Hardware-Software Co-designer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "embedded c", "firmware", "arm cortex", "freertos", "microcontroller", "spi i2c uart", "register level programming", "stm32".
- **Contextual Inferences**: Bare-metal C repositories, HAL drivers, FreeRTOS configurations, Keil/PlatformIO/Makefile embedded targets.
- **Chained Predecessors**: `task-decomposition`, `root-cause-debugging`.

## 3. Explicit Exclusions
- Do NOT use when:
  - High-level web application frontend or cloud container orchestration.
  - Managed runtimes (Node.js, Python) on full operating systems without microcontrollers.

## 4. Required Inputs & Context
- Target microcontroller architecture (e.g. ARM Cortex-M0+/M4/M7, STM32, ESP32, nRF52).
- Hardware schematic, memory map (Flash/SRAM sizes), and clock tree setup.
- Communication bus specifications (baud rates, SPI clock polarity/phase).

## 5. Expected Outputs & Artifacts
- MISRA-C compliant firmware source and header files.
- Deterministic FreeRTOS task definitions with priority queues.
- Peripheral drivers (UART, SPI, I2C, DMA, ADC, GPIO) with memory-mapped register access.
- Linker script configuration (`.ld`) and static memory allocation verification.

## 6. Step-by-Step Operating Procedure
1. **Clock Tree & Peripheral Initialization**:
   - Configure Phase-Locked Loop (PLL) and bus prescalers (AHB/APB) for stable system clock (SysTick).
2. **Deterministic Memory Management**:
   - Forbid dynamic memory allocation (`malloc`/`free`) in real-time control loops. Use static ring buffers and FreeRTOS static allocation (`xTaskCreateStatic`).
3. **Interrupt Service Routine (ISR) Architecture**:
   - Keep ISRs minimal: acknowledge hardware flags, buffer received bytes, and defer heavy processing to high-priority tasks via binary semaphores (`xSemaphoreGiveFromISR`).
4. **Hardware Communication Protocols**:
   - Implement bus communication using Direct Memory Access (DMA) to avoid CPU polling overhead.
5. **Low-Power Modes & Watchdog**:
   - Implement Independent Watchdog (IWDG) refresh in the main loop to prevent device bricking.
   - Enter Sleep/Stop modes during idle tasks to conserve power.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of embedded toolchain:
  ```bash
  arm-none-eabi-gcc --version 2>/dev/null || echo "GCC ARM toolchain not in path"
  find . -name "*.ld" -o -name "FreeRTOSConfig.h" 2>/dev/null
  ```
- Preservation rule: Never block inside an Interrupt Service Routine (ISR) with delays or busy loops.

## 8. Tool & Dependency Requirements
- GNU Arm Embedded Toolchain (`arm-none-eabi-gcc`), OpenOCD, GDB, CMake/Make or PlatformIO.

## 9. Implementation Guidelines & Best Practices
- Declare hardware registers with `volatile` pointers to prevent compiler optimization dead-stripping.
- Enforce integer width types from `<stdint.h>` (`uint8_t`, `uint32_t`, `int16_t`) instead of native `int` or `long`.

```c
#include <stdint.h>
#include <stdbool.h>

#define UART_STATUS_REG   (*(volatile uint32_t *)(0x40013800))
#define UART_DATA_REG     (*(volatile uint32_t *)(0x40013804))
#define UART_TXE_FLAG     (1U << 7)

void UART_TransmitByte(uint8_t data) {
    // Wait until Transmit Data Register is Empty
    while (!(UART_STATUS_REG & UART_TXE_FLAG)) {
        // Optional watchdog kick or timeout counter
    }
    UART_DATA_REG = data;
}
```

## 10. Error Handling & Recovery Procedures
- HardFault Exception: Inspect Link Register (`LR`), Stack Pointer (`MSP`/`PSP`), and Configurable Fault Status Register (`CFSR`) to determine bus error, unaligned memory access, or stack overflow.
- FreeRTOS Stack Overflow: Enable `configCHECK_FOR_STACK_OVERFLOW = 2` and implement `vApplicationStackOverflowHook()`.

## 11. Security & Privacy Constraints
- Secure Boot: Verify cryptographic firmware image signatures (ECDSA P-256) before jumping to user flash vector table.
- Disable JTAG/SWD debug access in production flash option bytes to prevent firmware extraction.

## 12. Verification & Testing Requirements
- Compile firmware and check flash/RAM usage:
  ```bash
  arm-none-eabi-size build/firmware.elf
  ```
- Verify zero compiler warnings with `-Wall -Wextra -Werror -pedantic`.

## 13. Completion Criteria
- Firmware compiles cleanly within flash/RAM size boundaries.
- Peripheral drivers execute without race conditions or memory faults.
- Watchdog timer maintains system stability.

## 14. Relevant Official References
- ARM Cortex-M Programming Manual (ARM DDI 0403E).
- MISRA C:2012 Guidelines for the use of the C language in critical systems.
- FreeRTOS Real-Time Kernel Reference Manual.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Cortex-M0+, M3, M4, M7, M33 and RISC-V cores.
