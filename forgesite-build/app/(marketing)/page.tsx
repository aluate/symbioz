import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function MarketingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-[600px] flex items-center justify-center bg-gray-900 text-white">
        <div className="absolute inset-0 bg-black/50"></div>
        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Clean Websites for Builders & Trades
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-200">
            Get seen. Stay simple.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild className="bg-blue-600 hover:bg-blue-700 text-lg px-8 py-6">
              <Link href="/intake">Get a Website Plan</Link>
            </Button>
            <Button asChild variant="outline" className="border-white text-white hover:bg-white/10 text-lg px-8 py-6">
              <Link href="#examples">See Examples</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Why Builders Use Forge Site */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Why Builders Use Forge Site</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            {[
              { title: 'Home Builders', desc: 'Custom home construction companies' },
              { title: 'Remodelers', desc: 'Renovation and remodeling specialists' },
              { title: 'Cabinet Shops', desc: 'Custom cabinetry and millwork' },
              { title: 'Steel Buildings', desc: 'Commercial and agricultural structures' },
              { title: 'Trades', desc: 'HVAC, electrical, plumbing professionals' }
            ].map((item, idx) => (
              <div key={idx} className="bg-gray-50 p-6 rounded-lg text-center">
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-600 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* What You Get */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">What You Get</h2>
          <ul className="space-y-4 text-lg">
            {[
              'Done-for-you website (not DIY)',
              'Fast turnaround (3-7 days vs 6-12 weeks)',
              'Professional copywriting included',
              'Design and setup handled for you',
              'Lead capture forms built-in',
              'Mobile and SEO ready',
              'Trade-focused modules optimized for your industry'
            ].map((item, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-blue-600 mr-3">✓</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mt-12">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">1</div>
              <h3 className="text-xl font-semibold mb-2">Intake</h3>
              <p className="text-gray-600">Fill out a structured intake (or talk with our bot).</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">2</div>
              <h3 className="text-xl font-semibold mb-2">Build Phase</h3>
              <p className="text-gray-600">Our modules, copy system, and layout engine assemble your site.</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">3</div>
              <h3 className="text-xl font-semibold mb-2">Review</h3>
              <p className="text-gray-600">You review the preview and request small config changes.</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">4</div>
              <h3 className="text-xl font-semibold mb-2">Launch</h3>
              <p className="text-gray-600">We launch, connect your domain, and you're live.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-16 px-4 bg-gray-50" id="pricing">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Pricing</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Starter Run */}
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-2xl font-bold mb-2">Starter Run</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">$1,495</div>
              <ul className="space-y-3 mb-8">
                <li>4-6 pages</li>
                <li>Gallery module</li>
                <li>Contact & lead capture</li>
                <li>SEO setup</li>
                <li>Copywriting</li>
                <li>Most sites in 3-5 days after intake</li>
              </ul>
              <Button asChild className="w-full bg-blue-600 hover:bg-blue-700">
                <Link href="/intake">Get Started</Link>
              </Button>
            </div>

            {/* Workhorse Run */}
            <div className="bg-white p-8 rounded-lg shadow-md border-2 border-blue-600">
              <div className="text-sm font-semibold text-blue-600 mb-2">POPULAR</div>
              <h3 className="text-2xl font-bold mb-2">Workhorse Run</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">$2,950</div>
              <ul className="space-y-3 mb-8">
                <li>Everything in Starter</li>
                <li>Services database module</li>
                <li>Reviews/testimonials module</li>
                <li>Hiring page</li>
                <li>Financing page</li>
                <li>Most sites in 5-7 days after intake</li>
              </ul>
              <Button asChild className="w-full bg-blue-600 hover:bg-blue-700">
                <Link href="/intake">Get Started</Link>
              </Button>
            </div>

            {/* Premium Run */}
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-2xl font-bold mb-2">Premium Run</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">$6,950</div>
              <ul className="space-y-3 mb-8">
                <li>Everything in Workhorse</li>
                <li>Full media kit</li>
                <li>SEO content library</li>
                <li>Hiring pipeline</li>
                <li>Brochure generation</li>
                <li>Most sites in 7-10 days after intake</li>
              </ul>
              <Button asChild className="w-full bg-blue-600 hover:bg-blue-700">
                <Link href="/intake">Get Started</Link>
              </Button>
            </div>
          </div>

          {/* Support Plans */}
          <div className="mt-12 pt-12 border-t">
            <h3 className="text-2xl font-bold text-center mb-8">Support Plans</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg">
                <h4 className="font-semibold mb-2">Basic - $49/mo</h4>
                <p className="text-sm text-gray-600">Hosting + minor updates</p>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <h4 className="font-semibold mb-2">Pro - $99/mo</h4>
                <p className="text-sm text-gray-600">+ Analytics + form routing</p>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <h4 className="font-semibold mb-2">Premium - $199/mo</h4>
                <p className="text-sm text-gray-600">+ Blog posts + performance audits</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Examples */}
      <section className="py-16 px-4 bg-white" id="examples">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Examples</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { title: 'Builder Example', href: '/examples/builder', desc: 'Custom home builder site' },
              { title: 'Cabinet Shop', href: '/examples/cabinet-shop', desc: 'Custom cabinetry showcase' },
              { title: 'Steel Buildings', href: '/examples/steel-buildings', desc: 'Commercial structures' }
            ].map((example, idx) => (
              <Link key={idx} href={example.href} className="block bg-gray-50 p-6 rounded-lg hover:shadow-lg transition-shadow">
                <h3 className="text-xl font-semibold mb-2">{example.title}</h3>
                <p className="text-gray-600 mb-4">{example.desc}</p>
                <span className="text-blue-600 hover:underline">View Site →</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Modules We Build With */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Modules We Build With</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Hero Sections</h3>
              <p className="text-gray-600">Clear headlines. Strong CTAs. Built to convert.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Service Grids</h3>
              <p className="text-gray-600">Show what you do. Plain and clear.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Project Galleries</h3>
              <p className="text-gray-600">Showcase your work. Let the photos do the talking.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">Contact & Lead Capture</h3>
              <p className="text-gray-600">Forms that work. Simple and effective.</p>
            </div>
          </div>
        </div>
      </section>

      {/* About */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Built by Builders, for Builders</h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            We understand the construction industry because we've been in it. Our real construction background 
            means we write copy that resonates, design layouts that convert, and build sites that actually work 
            for your business. No agency fluff. Just results.
          </p>
        </div>
      </section>

      {/* Questions, Straight Answers */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Questions, Straight Answers</h2>
          <div className="space-y-4">
            {[
              { 
                q: 'Are you a web design agency?', 
                a: 'No. We build sites from proven layouts and modules instead of designing from scratch.' 
              },
              { 
                q: 'Can I get custom design work?', 
                a: 'Major custom design work requires a scoped upgrade or new build cycle. Small config changes (text, images, contact info) can be handled through our chat bot or support plan.' 
              },
              { 
                q: 'How many revisions do I get?', 
                a: 'Small config changes are allowed during the review phase and after launch (via support plans). Large redesigns or layout changes require a new build cycle or package upgrade.' 
              },
              { 
                q: 'How fast can I get a site?', 
                a: 'Most builds complete in 3-7 days after intake confirmation and payment. That\'s 6-12 weeks faster than traditional agencies.' 
              },
              { 
                q: 'What if I need more pages?', 
                a: 'You can upgrade your package or we can scope a new build cycle with additional pages. Our module system keeps pricing clear and predictable.' 
              }
            ].map((faq, idx) => (
              <div key={idx} className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="font-semibold mb-2">{faq.q}</h3>
                <p className="text-gray-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Start the Build */}
      <section className="py-16 px-4 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Start the Build</h2>
          <p className="text-xl mb-8 text-gray-200">
            Simple intake. Solid results.
          </p>
          <Button asChild className="bg-blue-600 hover:bg-blue-700 text-lg px-8 py-6">
            <Link href="/intake">Get a Website Plan</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
