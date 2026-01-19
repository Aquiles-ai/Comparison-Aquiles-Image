import asyncio
from openai import AsyncOpenAI
import base64
import time
from pathlib import Path
from typing import Literal

URL_MODAL="https://your-user--aquiles-image-server-serve.modal.run"

client = AsyncOpenAI(
    base_url=URL_MODAL, api_key="dummy-api-key"
)

async def gen_image(prompt: str, image_id: int):
    start_time = time.time()
    try:
        print(f"[GEN {image_id}] Sending request: '{prompt[:50]}'...")
        response = await client.images.generate(
            prompt=prompt,
            model="stabilityai/stable-diffusion-3.5-medium",
            size="1024x1024",
            response_format="b64_json",
            n=1,
        )
        elapsed = time.time() - start_time

        output_dir = Path("outputs_image")
        output_dir.mkdir(exist_ok=True)

        paths = []
        for idx, item in enumerate(response.data):
            image_path = output_dir / f"image_{prompt[:50]}_{image_id}_{idx}.png"
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(item.b64_json))
            paths.append(str(image_path))

        n = len(paths)

        print(f"[GEN {image_id}] Completed in {elapsed:.2f}s -> {len(paths)} images")

        return {
            "id": image_id,
            "prompt": prompt,
            "elapsed": elapsed,
            "paths": paths,
            "success": True,
            "n": n,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[GEN {image_id}] Error after {elapsed:.2f}s: {e}")

        return {
            "id": image_id,
            "prompt": prompt,
            "elapsed": elapsed,
            "error": str(e),
            "success": False,
            "n": 0,
        }

async def test_batch_inference(mode: Literal["16", "32"]):
    print("=" * 80)
    print("TEST: Batch Inference")
    print("=" * 80)

    prompts_16 = [
        "a green tree in a beautiful forest",
        "a orange sunset over the ocean",
        "a pink flamingo standing in water",
        "a brown dog playing in the park",
        "a red rose blooming in a garden",
        "a blue butterfly on a yellow flower",
        "a purple mountain at dawn",
        "a white swan gliding on a lake",
        "a golden wheat field under the sun",
        "a black cat sitting on a fence",
        "a silver moon over a desert",
        "a colorful parrot in the jungle",
        "a gray wolf howling at night",
        "a turquoise wave crashing on the shore",
        "a copper autumn leaf falling",
        "a crimson sky during twilight"
    ]


    prompts_32 = [
        "a green tree in a beautiful forest",
        "a orange sunset over the ocean",
        "a pink flamingo standing in water",
        "a brown dog playing in the park",
        "a red rose blooming in a garden",
        "a blue butterfly on a yellow flower",
        "a purple mountain at dawn",
        "a white swan gliding on a lake",
        "a golden wheat field under the sun",
        "a black cat sitting on a fence",
        "a silver moon over a desert",
        "a colorful parrot in the jungle",
        "a gray wolf howling at night",
        "a turquoise wave crashing on the shore",
        "a copper autumn leaf falling",
        "a crimson sky during twilight",
        "a emerald green forest canopy",
        "a sapphire blue waterfall",
        "a amber glowing firefly at dusk",
        "a ivory white elephant in savanna",
        "a ruby red cardinal on a branch",
        "a jade green bamboo forest",
        "a coral pink cherry blossoms",
        "a midnight blue starry sky",
        "a bronze statue in a plaza",
        "a lavender field in provence",
        "a aqua tropical fish in reef",
        "a chocolate brown bear in woods",
        "a pearl white clouds in sky",
        "a lime green palm tree on beach",
        "a magenta orchid in rainforest",
        "a sandy beige dunes at sunset"
    ]

    prompts = None
    if mode == "16":
        prompts = prompts_16
    elif mode == "32":
        prompts = prompts_32
    else:
        raise ValueError("Invalid option")

    print(f"\nSending {len(prompts)} concurrent requests...\n")
    start_time = time.time()
    tasks = []

    tasks = [
        gen_image(prompt, i)
        for i, prompt in enumerate(prompts)
    ]
    results = await asyncio.gather(*tasks)

    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"\nSuccessful: {len(successful)}/{len(results)}")
    print(f"Failed: {len(failed)}/{len(results)}")
    print(f"Total elapsed time: {total_time:.2f}s")

    if successful:
        avg_time = sum(r['elapsed'] for r in successful) / len(successful)
        min_time = min(r['elapsed'] for r in successful)
        max_time = max(r['elapsed'] for r in successful)

        print(f"\nGeneration timings:")
        print(f"   Average: {avg_time:.2f}s")
        print(f"   Minimum: {min_time:.2f}s")
        print(f"   Maximum: {max_time:.2f}s")

    print(f"\nDetails for each request:")
    for result in results:
        status = "SUCCESS" if result['success'] else "FAIL"
        print(f"   [{result['id']}] {status} {result['elapsed']:.2f}s - {result['prompt'][:40]}")

    print("\n" + "=" * 80)

async def main():
    await test_batch_inference("16") # I'm sending 16 images to be generated simultaneously

if __name__ == "__main__":
    asyncio.run(main())
