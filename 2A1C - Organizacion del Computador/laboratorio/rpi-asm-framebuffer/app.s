	.include "draw_functions.s"
	
	.equ SCREEN_WIDTH,   640
	.equ SCREEN_HEIGH,   480
	.equ BITS_PER_PIXEL, 32

	.equ GPIO_BASE,    0x3f200000
	.equ GPIO_GPFSEL0, 0x00
	.equ GPIO_GPLEV0,  0x34
	

	.globl main

main:

	mov x20, x0 				 // Store framebuffer base address to x20


// BACKGROUND
	// draw grass
	movz w10, #0x00, lsl #16
    movk w10, #0xbb00, lsl #00
	bl full_bg_paint


	// draw sky
	movz w10, #0x00, lsl 16
    movk w10, #0xddff, lsl 00
	bl upper_half_bg_paint


	// draw the sun
	mov x1, 100
	mov x2, 80
	movz w3, #0xff, lsl 16
	movk w3, #0xee00, lsl 00
	mov x4, 60
	bl draw_circle


// HOUSE
    // draw house
    mov x1, 400  				// x1: bottom left x coordinate
    mov x2, 100  				// x2: bottom left y coordinate
    mov x3, 200  				// x3: size of the square
	movz w10, #0xff, lsl 16
	movk w10, #0xcc00, lsl 00
    bl draw_square


	// draw roof
	mov x3, 500 // posicion esquina X
	mov x4, 70 // posicion esquina Y
	mov x5, 120 // altura
	movz w10, 0xcc, lsl 16
	movk w10, 0x2222, lsl 00
	bl draw_triangle


	// draw door
    mov x0, 500					// x0: bottom left x coordinate
    mov x1, 100					// x1: bottom left y coordinate
    mov x2, 570					// x2: top right x coordinate
    mov x3, 240					// x3: top right y coordinate
    mov x4, x20					// x4: framebuffer base address
	movz w10, #0xcc, lsl 16
	movk w10, #0x2222, lsl 00
    bl draw_rectangle
    
    
	// draw window
    mov x1, 420					// x1: bottom left x coordinate
    mov x2, 165					// x2: bottom left y coordinate
    mov x3, 60					// x3: size of the square
	movz w10, #0x00, lsl 16
	movk w10, #0xbbff, lsl 00
    bl draw_square


// CAR
	// draw top part
	mov x0, 90  				// x0: bottom left x coordinate 
    mov x1, 150  				// x1: bottom left y coordinate
    mov x2, 190  				// x2: top right x coordinate  
    mov x3, 210  				// x3: top right y coordinate
	movz w10, #0xdd, lsl 16
    movk w10, #0xdddd, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
    
    
    // draw bottom part
	mov x0, 50  				// x0: bottom left x coordinate 
    mov x1, 100  				// x1: bottom left y coordinate
    mov x2, 230  				// x2: top right x coordinate  
    mov x3, 160  				// x3: top right y coordinate
	movz w10, #0xdd, lsl 16
    movk w10, #0xdddd, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
    
    
    // draw left window
	mov x0, 100  				// x0: bottom left x coordinate 
    mov x1, 160  				// x1: bottom left y coordinate
    mov x2, 135  				// x2: top right x coordinate  
    mov x3, 200  				// x3: top right y coordinate
	movz w10, #0x00, lsl 16
    movk w10, #0xBBFF, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
    
    
    // draw right window
	mov x0, 145  				// x0: bottom left x coordinate 
    mov x1, 160  				// x1: bottom left y coordinate
    mov x2, 180  				// x2: top right x coordinate  
    mov x3, 200  				// x3: top right y coordinate
	movz w10, #0x00, lsl 16
    movk w10, #0xBBFF, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
	

	// draw left wheel
	mov x1, 100					// coords x
	mov x2,	380					// coords y
    mov w3, #0xFF000000
	mov x4, 25					// radius
	bl draw_circle


	// draw right wheel
	mov x1, 180					// coords x
	mov x2,	380					// coords y
    mov w3, #0xFF000000
	mov x4, 25					// radius
	bl draw_circle
	

// CHARACTER
	// draw head
	mov x1, 315					// coords x
	mov x2,	260					// coords y
    movz x3, #0xE5CC, lsl 0
    movk x3, #0xFFFF, lsl 16
	mov x4, 20					// radius
	bl draw_circle


	// draw eye
	mov x1, 320					// coords x
	mov x2,	257					// coords y
    mov w3, #0xFF000000
	mov x4, 5					// radius
	bl draw_circle


	// draw neck
    mov x0, 310  				// x0: bottom left x coordinate 
    mov x1, 190  				// x1: bottom left y coordinate
    mov x2, 320  				// x2: top right x coordinate  
    mov x3, 200  				// x3: top right y coordinate
	movz w10, #0xE5CC, lsl 0
    movk w10, #0xFFFF, lsl 16
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
	
	
	// draw torso
    mov x0, 300  				// x0: bottom left x coordinate 
    mov x1, 130  				// x1: bottom left y coordinate
    mov x2, 330  				// x2: top right x coordinate  
    mov x3, 190  				// x3: top right y coordinate
	movz w10, #0xcc, lsl 16
	movk w10, #0x2222, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle


	// draw arm
    mov x0, 310  				// x0: bottom left x coordinate 
    mov x1, 150  				// x1: bottom left y coordinate
    mov x2, 320  				// x2: top right x coordinate  
    mov x3, 180  				// x3: top right y coordinate
	movz w10, #0xA0, lsl 16
    movk w10, #0x0000, lsl 00 	
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle


	// draw hand
    mov x0, 310  				// x0: bottom left x coordinate 
    mov x1, 140  				// x1: bottom left y coordinate
    mov x2, 320  				// x2: top right x coordinate  
    mov x3, 150 				// x3: top right y coordinate
	movz w10, #0xE5CC, lsl 0 
    movk w10, #0xFFFF, lsl 16
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle
    
    
	// draw leg
    mov x0, 300  				// x0: bottom left x coordinate 
    mov x1, 70   				// x1: bottom left y coordinate
    mov x2, 330  				// x2: top right x coordinate
    mov x3, 130  				// x3: top right y coordinate
    movz w10, #0x00, lsl 16
    movk w10, #0xbbff, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle


	// draw feet
    mov x0, 330  				// x0: bottom left x coordinate 
    mov x1, 70  				// x1: bottom left y coordinate
    mov x2, 345  				// x2: top right x coordinate  
    mov x3, 80 					// x3: top right y coordinate
	movz w10, #0xA0, lsl 16
    movk w10, #0x0000, lsl 00
    mov x4, x20 				// x4: framebuffer base address
    bl draw_rectangle


	// Ejemplo de uso de gpios
	mov x9, GPIO_BASE

	// Atención: se utilizan registros w porque la documentación de broadcom
	// indica que los registros que estamos leyendo y escribiendo son de 32 bits

	// Setea gpios 0 - 9 como lectura
	str wzr, [x9, GPIO_GPFSEL0]

	// Lee el estado de los GPIO 0 - 31
	ldr w10, [x9, GPIO_GPLEV0]

	// And bit a bit mantiene el resultado del bit 2 en w10 (notar 0b... es binario)
	// al inmediato se lo refiere como "máscara" en este caso:
	// - Al hacer AND revela el estado del bit 2
	// - Al hacer OR "setea" el bit 2 en 1
	// - Al hacer AND con el complemento "limpia" el bit 2 (setea el bit 2 en 0)
	and w11, w10, 0b00000010

	// si w11 es 0 entonces el GPIO 1 estaba liberado
	// de lo contrario será distinto de 0, (en este caso particular 2)
	// significando que el GPIO 1 fue presionado

	//---------------------------------------------------------------
	// Infinite Loop

InfLoop:
	b InfLoop
