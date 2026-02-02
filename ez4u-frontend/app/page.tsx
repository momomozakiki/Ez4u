import DashboardLayout from './components/DashboardLayout';

export default function Home() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
          Welcome back!
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-zinc-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-700">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Users</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">1,234</p>
            <span className="text-sm text-green-600 dark:text-green-400 mt-2 block">+12% from last month</span>
          </div>
          
          <div className="bg-white dark:bg-zinc-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-700">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Sessions</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">56</p>
            <span className="text-sm text-green-600 dark:text-green-400 mt-2 block">+5% from last hour</span>
          </div>
          
          <div className="bg-white dark:bg-zinc-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-700">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">System Status</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">Healthy</p>
            <span className="text-sm text-gray-500 dark:text-gray-400 mt-2 block">All systems operational</span>
          </div>
        </div>

        <div className="mt-8 bg-white dark:bg-zinc-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center gap-4 py-3 border-b border-gray-100 dark:border-zinc-700 last:border-0">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">New user registered</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">2 minutes ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
