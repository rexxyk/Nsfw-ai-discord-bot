import torch
import sys
import os
import discord
import asyncio
from discord.ext import commands
from PIL import Image
import random

# Check if OptiX is available
try:
    import optix
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        raise RuntimeError("OptiX is available, but CUDA is not. Please make sure you have CUDA-enabled GPU drivers.")
except ImportError as e:
    raise RuntimeError("OptiX is not available. Please make sure you have OptiX installed and compatible GPU drivers.") from e

# Load the model
from diffusers import DiffusionPipeline

print("Loading model...")
model_id = "Niggendar/wildcardxREALNSFWSFW_nsfwSFW"
pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipeline.to(device)
print("Model loaded.")

# Create output folder if it doesn't exist
output_folder = r"C:\Users\ultra\Desktop\dddd\output"
os.makedirs(output_folder, exist_ok=True)

# Bot setup
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the options
gender_options = ["female"]
race_options = ["black", "white", "Latina", "Mexican", "Brazilian", "Swedish"]
hair_options = ["blonde", "brunette", "dirty blond", "black hair", "red hair", "blue hair"]
outfit_options = ["nude", "bikini", "micro bikini", "lace lingerie", "thong", "fishnet stockings", "corset", "g-string", "see-through leggings", "panties", "bra", "tank top", "crop top", "t-shirt", "jeans", "shorts", "latex outfit", "stripper heels"]
location_options = ["mall", "outdoor", "forest", "bed", "desk"]

# Counter for tracking the number of images generated
generated_image_count = 0

# Function to generate and save image
def generate_image(prompt, is_random=False):
    global generated_image_count
    generated_image_count += 1
    with torch.no_grad():
        image = pipeline(prompt).images[0]
    random_number = random.randint(1, 111111111110000000)  # Generate a random number
    prefix = "random" if is_random else "user"
    image_path = os.path.join(output_folder, f"generated_image_{prefix}_{random_number}.png")  # Append the random number to the image name
    image.save(image_path)
    return image_path

# Command for generating random images
@bot.command()
async def genrandom(ctx, num_images: int = 1):
    global generated_image_count
    generated_image_count = 0
    await ctx.send(f"Generating {num_images} random image(s)...")
    
    for i in range(num_images):
        # Generate a random prompt
        prompt = f"a photo of a {random.choice(gender_options)} {random.choice(race_options)} with {random.choice(hair_options)} hair wearing {random.choice(outfit_options)} in a {random.choice(location_options)}"
        image_path = generate_image(prompt, is_random=True)
        
        # Create an embedded message
        embed = discord.Embed(title="Generated Image", description=f"Prompt: {prompt}", color=0x0000FF)  # Blue color for random images
        embed.set_image(url=f"attachment://{os.path.basename(image_path)}")
        
        # Send the embedded message with the image
        await ctx.send(embed=embed, file=discord.File(image_path))
    
    await ctx.send(f"Generated {generated_image_count} random image(s).")

# Command for generating image with user-defined prompt
@bot.command()
async def gen(ctx, *, prompt):
    global generated_image_count
    generated_image_count = 0
    await ctx.send("Processing...")

    image_path = generate_image(prompt)
    
    # Create an embedded message
    embed = discord.Embed(title="Generated Image", description=f"Prompt: {prompt}", color=0x00FF00)  # Green color for user-defined images
    embed.set_image(url=f"attachment://{os.path.basename(image_path)}")
    
    # Send the embedded message with the image
    await ctx.send(embed=embed, file=discord.File(image_path))
    
    await ctx.send("Generated 1 image.")

# Event handler for bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
if __name__ == "__main__":
    token = "UR BOT TOKEN"  # Replace with your bot token
    bot.run(token)
