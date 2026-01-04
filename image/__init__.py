# Image nodes package
from .image_url_loader_node import NODE_CLASS_MAPPINGS as ImageURLLoader_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ImageURLLoader_DISPLAY_MAPPINGS
from .qwen_image_edit_node import NODE_CLASS_MAPPINGS as QwenImageEdit_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as QwenImageEdit_DISPLAY_MAPPINGS
from .wanx_image_generation_node import NODE_CLASS_MAPPINGS as WanxImageGen_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as WanxImageGen_DISPLAY_MAPPINGS
from .seedream_image_to_image_node import NODE_CLASS_MAPPINGS as SeedreamI2I_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SeedreamI2I_DISPLAY_MAPPINGS

NODE_CLASS_MAPPINGS = {
    **ImageURLLoader_MAPPINGS,
    **QwenImageEdit_MAPPINGS,
    **WanxImageGen_MAPPINGS,
    **SeedreamI2I_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **ImageURLLoader_DISPLAY_MAPPINGS,
    **QwenImageEdit_DISPLAY_MAPPINGS,
    **WanxImageGen_DISPLAY_MAPPINGS,
    **SeedreamI2I_DISPLAY_MAPPINGS,
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']