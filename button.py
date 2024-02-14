import pygame 

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()              # button width
		height = image.get_height()            # button height
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))       # resize
		self.rect = self.image.get_rect()      # Rect
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):         # Draw button + check mouse clicking => gives action
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):                # mouse is pointing to button
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:   # mouse is clicked       [0]: right click
				action = True          # apply action
				self.clicked = True    # button is clicked

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action