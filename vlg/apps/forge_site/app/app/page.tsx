export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-porcelain py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-graphite mb-6">
            Professional websites. Built fast. Done right.
          </h1>
          <p className="text-xl text-graphite/80 mb-8 max-w-2xl mx-auto">
            Forge Site builds clean, modern websites from your business information. No chaos. No months of meetings. Just a simple process that gets you online with a site you're proud to show.
          </p>
          <p className="text-lg text-steel-blue font-medium mb-8">
            Get seen. Stay simple.
          </p>
          <div className="flex gap-4 justify-center">
            <a
              href="#start"
              className="bg-steel-blue text-white px-8 py-3 rounded-lg font-medium hover:opacity-90 transition"
            >
              Start Your Site
            </a>
            <a
              href="#how-it-works"
              className="bg-lavender-gray text-graphite px-8 py-3 rounded-lg font-medium hover:opacity-90 transition"
            >
              See How It Works
            </a>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold text-graphite mb-6">
            Most websites are a mess.
          </h2>
          <div className="space-y-4 text-lg text-graphite/80">
            <p>
              You try to build it yourself. You get lost in drag-and-drop tools. Nothing looks right. You spend hours and it still looks amateur.
            </p>
            <p>
              Or you hire an agency. Months go by. Meetings stack up. The price keeps climbing. You're locked into a system you don't understand.
            </p>
            <p className="font-medium text-graphite">
              Neither works.
            </p>
            <p>
              You just want a website that looks professional and gets the job done. Without the headache.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-16 px-4 bg-porcelain">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold text-graphite mb-12 text-center">
            How Forge Site Works
          </h2>
          <div className="space-y-12">
            <div>
              <h3 className="text-2xl font-semibold text-graphite mb-4">
                Step 1: You fill in a short form.
              </h3>
              <p className="text-lg text-graphite/80">
                Tell us about your business. What you do. Where you work. What you want the site to accomplish. Simple questions. Plain answers.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-graphite mb-4">
                Step 2: We build your site.
              </h3>
              <p className="text-lg text-graphite/80">
                Our system picks the right template. Assembles proven modules. Writes clear copy. Applies professional styling. All based on what you told us.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-graphite mb-4">
                Step 3: You review, we tune, we launch.
              </h3>
              <p className="text-lg text-graphite/80">
                You see the site. We make adjustments. We deploy it. You're live.
              </p>
              <p className="text-lg font-medium text-graphite mt-2">
                That's it. Days, not months.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold text-graphite mb-12 text-center">
            Features
          </h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                Sites built on modules we already trust.
              </h3>
              <p className="text-graphite/80">
                Every layout is tested. Every component works. No experiments. No guesswork.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                Clean copy that sounds human, not corporate.
              </h3>
              <p className="text-graphite/80">
                We write in plain language. Short sentences. Strong verbs. Real talk.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                Designed to be edited later without blowing it up.
              </h3>
              <p className="text-graphite/80">
                You can update content. Swap images. Add pages. The structure stays solid.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                SEO-ready from day one.
              </h3>
              <p className="text-graphite/80">
                Proper headings. Meta tags. Structured data. Search engines understand your site.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                Mobile-friendly by default.
              </h3>
              <p className="text-graphite/80">
                Looks good on phones, tablets, desktops. Everywhere.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-graphite mb-2">
                Ready for Vercel deployment.
              </h3>
              <p className="text-graphite/80">
                One command and you're live. Or we handle it for you.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* For Whom */}
      <section className="py-16 px-4 bg-porcelain">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold text-graphite mb-8 text-center">
            For Whom
          </h2>
          <p className="text-lg text-graphite/80 mb-8 text-center">
            Forge Site works for:
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Builders and contractors</h3>
              <p className="text-graphite/80">who need to showcase their work and capture leads.</p>
            </div>
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Local service professionals</h3>
              <p className="text-graphite/80">— plumbers, electricians, HVAC, roofers — who want to look credible online.</p>
            </div>
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Small shops and boutiques</h3>
              <p className="text-graphite/80">selling products with a simple catalog and checkout.</p>
            </div>
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Designers and architects</h3>
              <p className="text-graphite/80">showcasing portfolios and building trust.</p>
            </div>
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Gyms and fitness studios</h3>
              <p className="text-graphite/80">promoting services and booking clients.</p>
            </div>
            <div className="bg-white p-6 rounded-lg">
              <h3 className="font-semibold text-graphite mb-2">Law practices and consultants</h3>
              <p className="text-graphite/80">establishing professional presence.</p>
            </div>
          </div>
          <p className="text-lg text-graphite/80 mt-8 text-center">
            If you're busy running your business and need a professional web presence, Forge Site is for you.
          </p>
        </div>
      </section>

      {/* Proof / Trust */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold text-graphite mb-6">
            Proof / Trust
          </h2>
          <div className="space-y-4 text-lg text-graphite/80">
            <p>
              We've built systems before. We know what works. We know what doesn't.
            </p>
            <p>
              Forge Site isn't our first website builder. It's our best one.
            </p>
            <p>
              We've taken everything we've learned about building sites that convert, look professional, and don't break — and we've made it into a system.
            </p>
            <p className="font-medium text-graphite">
              You get the benefit of that experience. Without the months of custom development.
            </p>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section id="start" className="py-20 px-4 bg-steel-blue text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to get online?
          </h2>
          <p className="text-xl mb-8 text-white/90">
            Fill out our intake form. We'll build your site. You'll see it in days.
          </p>
          <p className="text-lg mb-8 text-white/80">
            No long sales calls. No confusing proposals. Just a simple process that works.
          </p>
          <p className="text-xl font-medium mb-8">
            Get seen. Stay simple.
          </p>
          <div className="flex gap-4 justify-center">
            <a
              href="#start"
              className="bg-white text-steel-blue px-8 py-3 rounded-lg font-medium hover:opacity-90 transition"
            >
              Start Your Site
            </a>
            <a
              href="#examples"
              className="bg-lavender-gray text-graphite px-8 py-3 rounded-lg font-medium hover:opacity-90 transition"
            >
              See Examples
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-graphite text-porcelain py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h3 className="text-2xl font-semibold mb-2">Forge Site</h3>
            <p className="text-lg">Get seen. Stay simple.</p>
          </div>
          <div className="flex gap-8 mb-8">
            <a href="#about" className="hover:underline">About</a>
            <a href="#how-it-works" className="hover:underline">How It Works</a>
            <a href="#pricing" className="hover:underline">Pricing</a>
            <a href="#contact" className="hover:underline">Contact</a>
          </div>
          <p className="text-sm text-porcelain/60">
            © 2024 Forge Site. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  );
}

