from __future__ import annotations

import abc
import typing as ty

import aurcore as aur

if ty.TYPE_CHECKING:
   import discord
   from flux.flux import Flux
   from flux.flux import Command


class Context(abc.ABC, aur.util.AutoRepr):
   @property
   @abc.abstractmethod
   def guild(self) -> discord.Guild: ...

   @property
   def config_identifier(self) -> int:
      return self.guild.id


class GuildChannelContext(Context):
   def __init__(self, bot: Flux, channel: discord.abc.GuildChannel):
      self.flux = bot
      self.channel = channel

   @property
   def guild(self) -> discord.Guild:
      return self.channel.guild

   @property
   def me(self) -> discord.abc.User:
      return self.guild.me if self.guild else self.flux.user


class MessageContext(GuildChannelContext):
   def __init__(self, bot: Flux, message: discord.Message):
      self.message = message
      self.flux = bot
      self.command: ty.Optional[Command] = None

   @property
   def deprefixed_cont(self) -> str:
      return self.message.content.removeprefix(self.cfg["prefix"])

   @property
   def channel(self) -> discord.TextChannel:
      return self.message.channel

   @property
   def author(self) -> ty.Union[discord.User, discord.Member]:
      return self.message.author

   @property
   def config_identifier(self) -> int:
      return self.guild.id if self.guild else self.author.id

   @property
   def author_auth_ids(self) -> ty.List[int]:
      identifiers = [self.author.id]
      if self.guild:
         identifiers.extend([role.id for role in self.author.roles])
      return identifiers

   @property
   def args(self) -> ty.Optional[str]:
      if self.command and self.deprefixed_cont:
         return self.deprefixed_cont.removeprefix(self.command.name).lstrip()
      return None

   @property
   def config(self) -> ty.Dict[ty.Any, str]:
      return self.flux.CONFIG.of(self.config_identifier)

   @property
   def full_command(self) -> ty.Optional[str]:
      return f"{self.config['prefix']}{self.command.name}"
