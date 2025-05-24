Realized spaceshooter with "pygame"
Algorithm:
1. Download any images for our display, ships (*)
2. Create display, main ship and give him movement
3. Create enemy ships - give them movements
4. class Laser - give all ships do shooting
5. function collide - check collapses with enemies
6. Draw levels, lives labels into main font, do final checks

(*) Convert images for required sizes:

-our_image = Image.open('images/your.jpg')

-size_for_game = our_image.crop((0, 0, p1.width, p1.height)).resize((1200, 600))

-size_for_game.save('images/your_resized_img.jpg')
