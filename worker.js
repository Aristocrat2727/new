export default {
  async fetch(request) {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    let query = '';
    try {
      const body = await request.json();
      query = body.query || '';
    } catch (e) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
    }

    if (!query) {
      return new Response(JSON.stringify({ error: 'Empty query' }), { status: 400 });
    }

    // Пробуем Wikipedia API
    const wikiUrl = `https://ru.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
    
    try {
      const response = await fetch(wikiUrl, {
        headers: { 'User-Agent': 'ShadowAI/1.0' }
      });
      
      if (response.ok) {
        const data = await response.json();
        let answer = data.extract || '';
        if (answer) {
          return new Response(JSON.stringify({ answer: answer.substring(0, 1500), source: 'Wikipedia' }), {
            headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
          });
        }
      }
      
      // Если Wikipedia не дала ответ — ищем через DuckDuckGo
      const ddgUrl = new URL('https://api.duckduckgo.com/');
      ddgUrl.searchParams.set('q', query);
      ddgUrl.searchParams.set('format', 'json');
      ddgUrl.searchParams.set('no_html', '1');
      ddgUrl.searchParams.set('skip_disambig', '1');
      
      const ddgResponse = await fetch(ddgUrl.toString(), {
        headers: { 'User-Agent': 'ShadowAI/1.0' }
      });
      const ddgData = await ddgResponse.json();
      
      let answer = ddgData.AbstractText || '';
      if (!answer && ddgData.RelatedTopics?.length) {
        for (const topic of ddgData.RelatedTopics) {
          if (topic.Text) {
            answer = topic.Text;
            break;
          }
        }
      }
      
      if (!answer) {
        answer = `Ничего не найдено по запросу "${query}". Попробуй уточнить или поищи в браузере.`;
      }
      
      return new Response(JSON.stringify({ answer: answer.substring(0, 1500), source: 'DuckDuckGo' }), {
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
      
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }
};