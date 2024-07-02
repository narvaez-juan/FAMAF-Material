.ifndef DRAW_FUNCTIONS_S
DRAW_FUNCTIONS_S:

    .equ SCREEN_WIDTH,   640
	.equ SCREEN_HEIGH,   480
    .equ BITS_PER_PIXEL, 32


// pixel_address calculate the address of a pixel based on coords (x, y)
pixel_address:
    //  PARAMETERS
    //  x3  =   coords x
    //  x4  =   coords y
    sub sp, sp, #24
    str lr, [sp]
	str x3, [sp, #8]    
	str x4, [sp, #16]
	
	mov x0, SCREEN_WIDTH            //  x0 = 640
	mul x0, x0, x4                  //  x0 = y * 640
	add x0, x0, x3                  //  x0 = x + y * 640
    lsl x0, x0, #2                  //  x0 = 4 * (x + y * 640)
	add x0, x0, x20                 //  x0 = framebuffer base address + 4 * (x + y * 640)
    
    ldr lr, [sp]
	ldr x3, [sp, #8]
    ldr x4, [sp, #16]
    add sp, sp, #24
	ret


//  paint_pixel: draw pixel on (x, y) coordenates with some color
paint_pixel:
    //  PARAMETERS
    //      SCREEN_WIDTH
    //      x3  =   coords x
    //      x4  =   coords y
    //      x10 =   color

    sub sp, sp, #32
    str lr, [sp]
    str x0, [sp, #8]
    str x3, [sp, #16]
    str x4, [sp, #24]

    bl pixel_address
    str w10, [x0]					// Paint pixel x0 with x10 color

    ldr lr, [sp]
    ldr x0, [sp, #8]
    ldr x3, [sp, #16]
    ldr x4, [sp, #24]
    add sp, sp, #32
	ret


//  background_paint: paint screen divided in half <x3> times with <x10> color
background_paint:
	// PARAMETERS
    //      SCREEN_WIDTH
    //      SCREEN_HEIGH
    //      x3  =   divide screen in half <x3> times
    //      x10 =   color

    sub sp, sp, #32
    str lr, [sp]
    str x0, [sp, #8]
    str x1, [sp, #16]
    str x2, [sp, #24]

    mov x0, x20                     // Load framebuffer address
    mov x1, SCREEN_WIDTH
    mov x2, SCREEN_HEIGH
    lsr x2, x2, x3                  // Divide x2 by 2^(x3) times

loop_b1: 
    mov x1, SCREEN_WIDTH
loop_b0:
    stur w10, [x0]                  // Set pixel color
    add x0, x0, 4
    sub x1, x1, 1
    cbnz x1, loop_b0
    sub x2, x2, 1
    cbnz x2, loop_b1
    
end_background_paint:
    ldr lr, [sp] 
    ldr x0, [sp, #8]
    ldr x1, [sp, #16]
    ldr x2, [sp, #24]
    add sp, sp, #32
	ret


//  full_bg_paint: paint background with some color
full_bg_paint:
    //  PARAMETERS
    //      x10 =   color

    sub sp, sp, #16
    str lr, [sp]
    str x3, [sp, #8]
    mov x3, #0
    bl background_paint
    ldr lr, [sp]
    ldr x3, [sp, #8]
    add sp, sp, #16
	ret


//  upper_half_bg_paint: paint half background with some color
upper_half_bg_paint:
    // PARAMETERS
    //      x10 =   color

    sub sp, sp, #16
    str lr, [sp]
    str x3, [sp, #8]
    mov x3, #1
    bl background_paint
    ldr lr, [sp]
    ldr x3, [sp, #8]
    add sp, sp, #16
	ret

    
// draw_rectangle: draw a rectangle from bottom left (x, y) to top right (x, y)
draw_rectangle:
    //  PARAMETERS
    //      x0: bottom left x coordinate
    //      x1: bottom left y coordinate
    //      x2: top right x coordinate
    //      x3: top right y coordinate
    //      x4: beginning of framebuffer
    //      x10: color

    sub sp, sp, #40
    str lr, [sp]
    str x0, [sp, #8]
    str x19, [sp, #16]
    str x20, [sp, #24]
    str x21, [sp, #32]

    mov     x19, (SCREEN_HEIGH - 1)
    sub     x19, x19, x3                // x19 = first row from top
    mov     x20, SCREEN_WIDTH
    mul     x19, x19, x20               // x19 = initial vertical offset
    add     x19, x19, x0                // x19 = initial vertical offset + initial horizontal offset
    lsl     x19, x19, 2                 // x19 = total offset
    add     x4, x4, x19               
    mov     x28, x0
    mov     x0, x4                      // x0 = &framebuffer['rectangle's top left pixel']

    sub     x19, x2, x28                // x19 = rectangle width - 1
    add     x19, x19, 1                 // x19 = rectangle width
    sub     x20, x20, x19               // x20 = pixels between the end of a row and the beginning of the next row
    lsl     x20, x20, 2                 // x20 = bytes between the end of a row and the beginning of the next row

loop_r0:
    mov     x21, x19                    // x21 = rectangle width

loop_r1:
    str     w10, [x0]                   // Paint pixel
    add     x0, x0, 4                   // Advance to next pixel

    subs    x21, x21, 1                 // Check if we finished current row
    b.gt    loop_r1 					// If not, then draw next column

    add     x0, x0, x20                 // Advance to beginning of next row
    add     x1, x1, 1
    cmp     x1, x3
    b.le    loop_r0

    ldr lr, [sp]
    ldr x0, [sp, #8]
    ldr x19, [sp, #16]
    ldr x20, [sp, #24]
    ldr x21, [sp, #32]
    add sp, sp, #40
	ret


// draw_square: draw a square from bottom left (x, y) of some size
draw_square:
    //  PARAMETERS
    //      x0: beginning of framebuffer
    //      x1: bottom left x coordinate
    //      x2: bottom left y coordinate 
    //      x3: size
    //      x10: color
    sub sp, sp, #48
    str lr, [sp]
    str x0, [sp, #8]
    str x1, [sp, #16]
    str x2, [sp, #24]
    str x3, [sp, #32]

    mov     x4, x20					// Move framebuffer base address to x4
    sub     x3, x3, 1				// Top right (x', y') = (x + size - 1, y + size - 1)
    add     x0, x2, x3				// Set x3 to top right y coordinate
    add     x3, x1, x3				// Set x2 to top right x coordinate

    mov x16, x0
    mov x0, x1
    mov x1, x2
    mov x2, x3
    mov x3, x16

    bl      draw_rectangle			// Call draw_rectangle

    ldr lr, [sp]
    ldr x0, [sp, #8]
    ldr x1, [sp, #16]
    ldr x2, [sp, #24]
    ldr x3, [sp, #32]
    sub sp, sp, #48
	ret
	
	
// draw_circle: draw a circle based on (x, y) coords and a radius
draw_circle:
    //  PARAMETERS
    //      x0 : dirección FB
    //      x1 : coordenada x centro
    //      x2 : coordenada y centro
    //      x3 : color
    //      x4 : radio*/
	sub sp, sp, #16
	str lr, [sp, #8]
	str x5, [sp]
    mov x0, x20
	mul x5, x4, x4  						// x5 = r^2
	mov x9, x1 								// x center
	mov x10, x2 							// y center
	add x11, x1, x4 						// x max = x center + r
	add x12, X2, x4 						// y max = y center + r
	sub x1, x1, x4 							// initial x

	loop_c0:
		cmp x1, x11  						// compare x xmax
		b.ge end_loop_c0
		sub x2, x10, x4 					// restart y to initial position

		loop_c1: 							// advance in y
			cmp x2, x12
			b.ge end_loop_c1
			sub x13, x1, x9 				// (x-a)
			smull x13, w13, w13 			// (x-a)^2
			sub x14, x2, x10 				// (y-b)
			smull x14, w14, w14 			// (y-b)^2
			add x13, x13, x14 				// (x-a)^2 + (y-b)^2
			cmp x13, x5 					// compare with r^2
			b.ge skip_pixel
			bl aux_draw_pixel
			
			skip_pixel:
			add x2, x2, #1 					// advance in y
			b loop_c1
      
    	end_loop_c1:
			add x1, x1, #1 					// advance in x
			b loop_c0
	end_loop_c0:
		mov x1, x9
		mov x2, x10
		ldur lr, [sp, #8]
		ldur x5, [sp]
		add sp, sp, #16
	ret


    // draw_triangle: draw triangle on (x, y) coordenates with some height
draw_triangle:
    //  PARAMETERS 
    //      x3  =   coords x
    //      x4  =   coords y
    //      x5  =   height
    //      x10 =   color

	sub sp, sp, #40
	str lr, [sp]	
	str x3, [sp, #8]
	str x4, [sp, #16]
    str x5, [sp, #24]
    str x9, [sp, #32]
	
	mov x1, x3
	mov x2, x4
	mov x9, x3
	
loop_t0:
	mov x3, x9
loop_t1:
	bl paint_pixel
	add x3, x3, 1
	cmp x3, x1
	b.le loop_t1
	sub x9, x9, 1
	add x1, x1, 1
	add x4, x4, 1
	sub x5, x5, 1
	cbnz x5, loop_t0

	ldr lr, [sp]
	ldr x3, [sp, #8]
	ldr x4, [sp, #16]
    ldr x5, [sp, #24]
    ldr x9, [sp, #32]
	add sp, sp, #40
	ret


// draw_circle auxiliar function
aux_draw_pixel:
	mov x27, SCREEN_WIDTH
    mul x27, x27, x2
    add x27, x27, x1
    lsl x27, x27, 2
    add x27, x27, x20
	str w3, [x27]
	ret
    
    
.endif

