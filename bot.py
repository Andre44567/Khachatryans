// ===== USERS =====
let users = new Set();

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const text = (msg.text || '').trim();

  users.add(chatId);

  // ===== START + IMAGE =====
  if (text.startsWith('/start')) {
    return msg.send({
      photo: 'https://telegra.ph/file/6e7f0f9c1c2c3d4e5f6a7.jpg', // փոխի քո նկարով
      caption:
        '👋 Բարի գալուստ\n\n' +
        '📥 Ուղարկի link:\n' +
        '• TikTok 🎥\n' +
        '• YouTube 🎵\n' +
        '• Instagram 📸\n\n' +
        '📢 /broadcast text'
    });
  }

  // ===== BROADCAST =====
  if (text.startsWith('/broadcast ')) {
    const message = text.replace('/broadcast ', '');

    for (let id of users) {
      try {
        await bot.send(id, message);
      } catch (e) {}
    }

    return msg.reply('✅ Ուղարկվեց բոլորին');
  }

  // ===== TIKTOK =====
  if (text.includes('tiktok.com')) {
    try {
      let url = text;

      if (text.includes('vt.tiktok.com')) {
        let res = await fetch(text, { redirect: 'follow' });
        url = res.url;
      }

      let res = await fetch('https://tikwm.com/api/?url=' + encodeURIComponent(url));
      let data = await res.json();

      if (!data?.data?.play) {
        return msg.reply('❌ Չգտնվեց TikTok video');
      }

      return msg.send({
        video: data.data.play,
        caption: '🎥 TikTok video'
      });

    } catch {
      return msg.reply('❌ TikTok error');
    }
  }

  // ===== INSTAGRAM =====
  if (text.includes('instagram.com')) {
    try {
      let res = await fetch('https://igram.world/api/ig?url=' + encodeURIComponent(text));
      let data = await res.json();

      if (!data?.result?.[0]?.url) {
        return msg.reply('❌ Չգտնվեց Instagram media');
      }

      return msg.send({
        video: data.result[0].url,
        caption: '📸 Instagram media'
      });

    } catch {
      return msg.reply('❌ Instagram error');
    }
  }

  // ===== YOUTUBE =====
  if (text.includes('youtube.com') || text.includes('youtu.be')) {
    let link = 'https://api.vevioz.com/api/button/mp3?url=' + encodeURIComponent(text);

    return msg.reply(
      '🎵 Քաշելու համար սեղմի 👇\n' + link
    );
  }

  // ===== DEFAULT =====
  msg.reply('📩 Ուղարկի link կամ գրի /start');
});
