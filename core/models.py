from dataclasses import  dataclass
from typing import List, Union, Dict, Callable, Any
# from srint.core.response import Response
@dataclass
class Config:
    views_path: str 
    routes: List[Dict[str, Union[str, Callable[[Any], Any]]]]
    port: int
    host: str = "0.0.0.0"